from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order, OrderItem, Part
from datetime import datetime
from django.utils.timezone import make_aware

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