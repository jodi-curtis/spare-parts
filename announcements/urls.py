from django.urls import path
from . import views
from .views import AnnouncementsListView, AnnouncementsCreateView

urlpatterns = [
    path('', AnnouncementsListView.as_view(), name='announcements'),
    path('announcements/new/', AnnouncementsCreateView.as_view(), name='announcement-create'),
]