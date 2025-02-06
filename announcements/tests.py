from django.test import TestCase
from django.contrib.auth.models import User
from .models import Announcements
from datetime import datetime
from django.utils.timezone import make_aware

# Create your tests here.
class AnnouncementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.announcement = Announcements.objects.create(posted_by=self.user, message="This is an announcement", visible=True)

    def test_part_creation(self):
        self.assertEqual(self.announcement.posted_by.username, "testuser")
        self.assertEqual(self.announcement.message, "This is an announcement")
        self.assertEqual(self.announcement.visible, True)
