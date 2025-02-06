from django.test import TestCase
from django.contrib.auth.models import User
from .models import Part

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

