from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Part
from django.urls import reverse

# Create your tests here.
class PartModelTest(TestCase):
    def setUp(self):
        self.part = Part.objects.create(code="ABC123", name="Test Part", num_in_stock=10, low_stock_warning=2, location="AA-BB-11")

    def test_part_creation(self):
        self.assertEqual(self.part.code, "ABC123")
        self.assertEqual(self.part.name, "Test Part")
        self.assertEqual(self.part.num_in_stock, 10)
        self.assertEqual(self.part.low_stock_warning, 2)
        self.assertEqual(self.part.location, "AA-BB-11")

class PartViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.store_manager = User.objects.create_user(username="store_manager", password="testpassword")
        self.store_manager.profile.user_group = "store_manager"
        self.store_manager.profile.save()

        self.engineer = User.objects.create_user(username="engineer", password="testpassword")
        self.engineer.profile.user_group = "engineer"
        self.engineer.profile.save()

        self.part1 = Part.objects.create(code="TP123", name="Test Part1",  num_in_stock=5,  low_stock_warning=2, location="AA-BB-11")
        self.part2 = Part.objects.create(code="TP321", name="Test Part2",  num_in_stock=10,  low_stock_warning=1, location="AA-BB-22")
        self.part3 = Part.objects.create(code="TP111", name="Test Part3",  num_in_stock=1,  low_stock_warning=3, location="AA-BB-33")


    # Test Store manager brought their dashboard on login
    def test_store_manager_login_redirect(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.get(reverse("login-success"))
        self.assertRedirects(response, reverse("order-home"))

    # Test Engineer brought their dashboard on login
    def test_engineer_login_redirect(self):
        self.client.login(username="engineer", password="testpassword")
        response = self.client.get(reverse("login-success"))
        self.assertRedirects(response, reverse("parts-home"))
        
    # Test part list view
    def test_part_list_view(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.get(reverse('parts-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Part1')
        self.assertTemplateUsed(response, 'parts/part_list.html')

    # test searching for part on list view
    def test_part_list_search(self):
        self.client.login(username="engineer", password="testpassword")
        response = self.client.get(reverse('parts-list'), {"searchVal": "321"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Part2')


    # Test part detail view
    def test_part_detail_view(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.get(reverse('part-detail', args=[self.part1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Part1')
        self.assertNotContains(response, 'Test Part2')

    # Test engineer can order part when stock available
    def test_part_detail_order_in_stock(self):
        self.client.login(username="engineer", password="testpassword")
        response = self.client.post(reverse("part-detail", args=[self.part2.id]), {"order_quantity": 2})
        self.part2.refresh_from_db()
        self.assertEqual(self.part2.num_in_stock, 8)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Added to order")

    # Test engineer can't order part when stock unavailable
    def test_part_detail_order_not_in_stock(self):
        self.client.login(username="engineer", password="testpassword")
        response = self.client.post(reverse("part-detail", args=[self.part1.id]), {"order_quantity": 6})
        self.part1.refresh_from_db()
        self.assertEqual(self.part1.num_in_stock, 5)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Not enough stock available")

    # Test store manager can receipt parts into stock
    def test_part_detail_receipt_stock(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.post(reverse("part-detail", args=[self.part2.id]), {"receipt_quantity": 3})
        self.part2.refresh_from_db()
        self.assertEqual(self.part2.num_in_stock, 13)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Stock updated successfully!")


    # Test low stock view
    def test_low_stock_view(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.get(reverse('low-stock'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Part3')
        self.assertTemplateUsed(response, 'parts/low_stock.html')

    # Test creating part
    def test_part_create_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.get(reverse('part-create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('part-create'), {'code': '111', 'name':'TestP1', 'num_in_stock':4, 'low_stock_warning':2, 'location':'AA-BB-CC'})
        self.assertRedirects(response, reverse('parts-list'))
        self.assertEqual(Part.objects.count(), 4)

    # Test updating part
    def test_part_update_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.get(reverse('part-update', args=[self.part1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('part-update', args=[self.part1.id]),{'code': self.part1.code,'name': self.part1.name,'num_in_stock': self.part1.num_in_stock,'low_stock_warning': 3,'location': self.part1.location})
        self.part1.refresh_from_db()
        self.assertEqual(self.part1.low_stock_warning, 3)
        self.assertRedirects(response, reverse('part-detail', args=[self.part1.id]))
    
    # Test deleting part
    def test_part_delete_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.post(reverse('part-delete', args=[self.part1.id]))
        self.assertEqual(Part.objects.count(), 2)
        self.assertRedirects(response, reverse('parts-list'))