from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Announcements
from datetime import datetime
from django.utils.timezone import make_aware
from django.urls import reverse

# Create your tests here.
class AnnouncementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.announcement = Announcements.objects.create(posted_by=self.user, message="This is an announcement", visible=True)

    def test_announcement_creation(self):
        self.assertEqual(self.announcement.posted_by.username, "testuser")
        self.assertEqual(self.announcement.message, "This is an announcement")
        self.assertEqual(self.announcement.visible, True)

class AnnouncementViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.store_manager = User.objects.create_user(username="store_manager", password="testpassword")
        self.store_manager.profile.user_group = "store_manager"
        self.store_manager.profile.save()

        self.engineer = User.objects.create_user(username="engineer", password="testpassword")
        self.engineer.profile.user_group = "engineer"
        self.engineer.profile.save()

        self.announcement = Announcements.objects.create(message="Test Announcement", posted_by=self.store_manager, visible=True)

    #Test list view loads
    def test_announcements_list_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.get(reverse('announcements'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Announcement")

    #Test can create announcement
    def test_announcement_create_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.get(reverse('announcement-create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcement-create'), {'message': 'New announcement message'})
        self.assertRedirects(response, reverse('announcements'))
        self.assertEqual(Announcements.objects.count(), 2)

    #Test can update announcement
    def test_announcement_update_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.get(reverse('announcement-update', args=[self.announcement.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('announcement-update', args=[self.announcement.id]), {'message': 'Updated message'})
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.message, 'Updated message')
        self.assertRedirects(response, reverse('announcements'))

    #Test can delete annoucement
    def test_announcement_delete_view(self):
        self.client.login(username='store_manager', password='testpassword')
        response = self.client.post(reverse('announcement-delete', args=[self.announcement.id]))
        self.assertEqual(Announcements.objects.count(), 0)
        self.assertRedirects(response, reverse('announcements'))

    # Test can updae visible status of announcement
    def test_announcement_post_toggle(self):
        self.client.login(username='store_manager', password='testpassword')
        self.assertTrue(self.announcement.visible)
        response = self.client.post(reverse('announcements'), {'announcement_id': self.announcement.id})
        self.announcement.refresh_from_db()
        self.assertFalse(self.announcement.visible)