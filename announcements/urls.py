from django.urls import path
from . import views
from .views import AnnouncementsListView, AnnouncementsCreateView, AnnouncementsUpdateView, AnnouncementDeleteView

urlpatterns = [
    path('', AnnouncementsListView.as_view(), name='announcements'),
    path('announcements/new/', AnnouncementsCreateView.as_view(), name='announcement-create'),
    path('announcements/<int:pk>/update/', AnnouncementsUpdateView.as_view(), name='announcement-update'),
    path('announcements/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
]