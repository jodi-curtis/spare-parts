from django.db import models

# Create your models here.
class Part(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    num_in_stock = models.PositiveIntegerField(default=0)
    low_stock_warning = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=10, help_text="Format: AB-A-5")

    # Method to check if stock is at or lower than the low stock warning
    def is_low_stock(self):
        return self.num_in_stock <= self.low_stock_warning

    def __str__(self):
        return self.name