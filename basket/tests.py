from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Basket, BasketItem, Part
from orders.models import Order
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime

# Create your tests here.
class BasketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.basket = Basket.objects.create(user=self.user)
    
    def test_basket_creation(self):
        self.assertEqual(self.basket.user.username, "testuser")
        self.assertEqual(self.basket.user, self.user)


class BasketItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.basket = Basket.objects.create(user=self.user)
        self.part = Part.objects.create(code="ABC123", name="Test Part", num_in_stock=10, low_stock_warning=2, location="AA-BB-11")
        self.basketitem = BasketItem.objects.create(basket=self.basket, part=self.part, quantity=1)
    
    def test_basketitem_creation(self):
        self.assertEqual(self.basketitem.basket, self.basket)
        self.assertEqual(self.basketitem.part, self.part)
        self.assertEqual(self.basketitem.quantity, 1)

class BasketViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.store_manager = User.objects.create_user(username="store_manager", password="testpassword")
        self.store_manager.profile.user_group = "store_manager"
        self.store_manager.profile.save()

        self.engineer = User.objects.create_user(username="engineer", password="testpassword")
        self.engineer.profile.user_group = "engineer"
        self.engineer.profile.save()

        self.part = Part.objects.create(code="TP123", name="Test Part",  num_in_stock=5,  low_stock_warning=2, location="AA-BB-11")

        self.basket = Basket.objects.create(user=self.engineer)

        self.basket_item = BasketItem.objects.create(basket=self.basket, part=self.part, quantity=2)

    # Test basket page loads and contains part
    def test_basket_page(self):
        self.client.login(username='engineer', password='testpassword')
        response = self.client.get(reverse('basket-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, "Test Part")
        self.assertTrue(BasketItem.objects.filter(basket=self.basket, part=self.part, quantity=2).exists())

    #Test removing items from basket 
    def test_remove_item_from_basket(self):
        self.client.login(username='engineer', password='testpassword')
        response = self.client.post(reverse('basket-home'), {'remove_item_id': self.basket_item.id})
        self.part.refresh_from_db()
        self.assertEqual(self.part.num_in_stock, 7)
        self.assertFalse(BasketItem.objects.filter(id=self.basket_item.id).exists())
        self.assertRedirects(response, reverse('basket-home'))

    # Test placing order moves items to order
    def test_place_order_moves_items_to_order(self):
        self.client.login(username='engineer', password='testpassword')

        collection_time = make_aware(datetime(2025, 2, 6, 14, 0))
        response = self.client.post(reverse('basket-home'), {'collection_datetime': collection_time})

        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.engineer)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 2)

        self.assertEqual(BasketItem.objects.count(), 0)
        self.assertRedirects(response, reverse('basket-home'))