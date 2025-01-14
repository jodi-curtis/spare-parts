from django.urls import path
from . import views
from .views import PartListView, PartDetailView, LowStockListView

urlpatterns = [
    path('', views.home, name='parts-home'),
    path('list/', PartListView.as_view(), name='parts-list'),
    path('list/<int:pk>', PartDetailView.as_view(), name='part-detail'),
    path('low-stock/', LowStockListView.as_view(), name='low-stock')
]