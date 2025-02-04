from django.db import models
from users.models import User

# Create your models here.
class Announcements(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement')
    message = models.TextField()
    visible = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message