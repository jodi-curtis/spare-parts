from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Order, OrderItem, Part
from datetime import datetime
from django.utils.timezone import make_aware
from django.urls import reverse


# Create your tests here.
class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.collection_datetime = make_aware(datetime(2025, 1, 15, 10, 30, 0))
        self.order = Order.objects.create(user=self.user, collection_datetime=self.collection_datetime, status="in_progress")

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.collection_datetime, self.collection_datetime)
        self.assertEqual(self.order.status, "in_progress")

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.collection_datetime = make_aware(datetime(2025, 1, 15, 10, 30, 0))
        self.order = Order.objects.create(user=self.user, collection_datetime=self.collection_datetime, status="in_progress")
        self.part = Part.objects.create(code="ABC123", name="Test Part", num_in_stock=10, low_stock_warning=2, location="AA-BB-11")
        self.orderitem = OrderItem.objects.create(order=self.order, part=self.part, quantity=1)
    
    def test_orderitem_creation(self):
        self.assertEqual(self.orderitem.order, self.order)
        self.assertEqual(self.orderitem.part, self.part)
        self.assertEqual(self.orderitem.quantity, 1)


class OrderListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.store_manager = User.objects.create_user(username="store_manager", password="testpassword")
        self.store_manager.profile.user_group = "store_manager"
        self.store_manager.profile.save()
        
        # Create orders with different statuses
        self.collection_datetime = make_aware(datetime(2025, 1, 15, 10, 30, 0))
        self.order1 = Order.objects.create(user=self.store_manager, collection_datetime=self.collection_datetime, status='in_progress')
        self.order2 = Order.objects.create(user=self.store_manager, collection_datetime=self.collection_datetime, status='collected')
        self.order3 = Order.objects.create(user=self.store_manager, collection_datetime=self.collection_datetime, status='in_progress')

    # Test collected orders are not shown on order screen
    def test_order_list_filtered(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.get(reverse('order-home'))
        orders = response.context['orders']
        self.assertNotIn(self.order2, orders)
        self.assertIn(self.order1, orders)
        self.assertIn(self.order3, orders)

    # Test store manager can update order status
    def test_update_order_status(self):
        self.client.login(username="store_manager", password="testpassword")
        response = self.client.post(reverse('order-home'), {'order_id': self.order1.id, 'new_status': 'ready'})
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.status, 'ready')
        self.assertRedirects(response, reverse('order-home'))