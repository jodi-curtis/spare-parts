from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    USER_GROUPS = [
        ('engineer', 'Engineer'),
        ('store_manager', 'Store Manager'),
    ]
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_group = models.CharField(max_length=100, choices=USER_GROUPS, default='engineer') #default to engineer

    def __str__(self):
        return f'{self.user.username} Profile'