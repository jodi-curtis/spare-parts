from django.urls import path
from . import views
from .views import PartListView, PartDetailView, PartCreateView, PartUpdateView, PartDeleteView, LowStockListView

urlpatterns = [
    path('', views.login_success, name='login-success'),
    path('dashboard/', views.home, name='parts-home'),
    path('list/', PartListView.as_view(), name='parts-list'),
    path('list/<int:pk>', PartDetailView.as_view(), name='part-detail'),
    path('part/new/', PartCreateView.as_view(), name='part-create'),
    path('part/<int:pk>/update/', PartUpdateView.as_view(), name='part-update'),
    path('part/<int:pk>/delete/', PartDeleteView.as_view(), name='part-delete'),
    path('low-stock/', LowStockListView.as_view(), name='low-stock')
]