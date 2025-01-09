from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='parts-home'),
    path('list/', views.parts, name='parts-list'),
]