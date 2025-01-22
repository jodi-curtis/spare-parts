from django.urls import path
from . import views
from .views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-home'),
]