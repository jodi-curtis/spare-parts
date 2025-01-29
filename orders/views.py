from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login

# Create your views here.
class OrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        # Filter orders to exclude those which have been collected
        return Order.objects.exclude(status='collected')

    def post(self, request, *args, **kwargs):
        if 'new_status' in request.POST:
            # Get order id
            order_id = request.POST.get('order_id')
            # Get status order should be set to
            new_status = request.POST.get('new_status')
            # Get order by order id
            order = Order.objects.get(id=order_id)
            # Update orders status
            order.status = new_status
            # Save order
            order.save()
            # Refresh page
            return redirect('order-home')
        
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to access the Order Screen")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())