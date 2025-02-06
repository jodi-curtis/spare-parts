from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

# Create your tests here.
class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.user_group, "engineer")