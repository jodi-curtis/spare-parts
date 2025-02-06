from django.test import TestCase
from django.contrib.auth.models import User
from .models import Basket, BasketItem, Part

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