from django.urls import path
from . import views
from .views import PartListView

urlpatterns = [
    path('', views.home, name='parts-home'),
    path('list/', PartListView.as_view(), name='parts-list'),
]