from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Part
from basket.models import Basket, BasketItem
from orders.models import Order
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    # Create empty dictionaries to store past and current orders
    past_orders = []
    current_orders = []

    # Get all orders for current user
    orders = Order.objects.filter(user = request.user)

    # Sort orders by status and add to relevent dictonary
    for order in orders:
        if order.status == 'collected':
            past_orders.append(order)
        else:
            current_orders.append(order)

    context = {
        'title': 'Home',
        'past_orders': past_orders,
        'current_orders': current_orders,
        'past_orders_count': len(past_orders), # Count number of past orders
        'current_orders_count': len(current_orders) # Count number of current orders
    }
    return render(request, 'parts/home.html', context)

class PartListView(ListView):
    model = Part
    context_object_name = 'parts'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get seach value, if not set set as empty
        search_value = self.request.GET.get('searchVal', '')
        # If search value exists, filter parts where code or name contains search value
        if search_value:
            queryset = queryset.filter(Q(code__icontains=search_value) | Q(name__icontains=search_value))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search value to context
        context['search_value'] = self.request.GET.get('searchVal', '')
        return context
    
class PartDetailView(DetailView):
    model = Part

    def post(self, request, *args, **kwargs):
        current_part = self.get_object()

        if 'receipt_quantity' in request.POST:
            # Get receipt quantity from form, if not set, set as 0
            quantity = int(request.POST.get('receipt_quantity', 0))
            # Add quantity to parts stock
            current_part.num_in_stock += quantity
            current_part.save()
            messages.success(request, f"Stock updated successfully!")

        if 'order_quantity' in request.POST:
            # Get quantity to add to order from form
            quantity = int(request.POST.get('order_quantity'))
            if quantity > 0:
                # Don't allow user to add more to their order than is in stock
                if quantity > current_part.num_in_stock:
                    messages.error(request, "Not enough stock available")
                else:
                    # Subtract quantity from parts stock
                    current_part.num_in_stock -= quantity
                    current_part.save()

                    # Fetch or create a basket for the logged-in user
                    basket, created = Basket.objects.get_or_create(user=self.request.user)
                    
                    # Fetch or create basket item for the logged-in user
                    basket_item, created = BasketItem.objects.get_or_create(basket=basket, part=current_part, defaults={'quantity':quantity})

                    # If part is already in basket, update quantity
                    if not created:
                        basket_item.quantity+=quantity
                        basket_item.save()

                    messages.success(request, f"Added to order")

        return redirect('part-detail', pk=current_part.pk)
    

class LowStockListView(ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'parts/low_stock.html'

    def get_queryset(self):
        all_parts = Part.objects.all()
        # Filter parts to only show those low in stock
        low_stock_parts = [part for part in all_parts if part.is_low_stock()]
        return low_stock_parts