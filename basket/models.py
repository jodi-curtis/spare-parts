from django.db import models
from parts.models import Part
from users.models import User

# Create your models here.
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)