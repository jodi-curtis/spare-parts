from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order
from django.views.generic import ListView

# Create your views here.

def home(request):
    return HttpResponse('<h1>Orders Home</h1>')

class OrderListView(ListView):
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