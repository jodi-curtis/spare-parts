from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Part
from basket.models import Basket, BasketItem
from orders.models import Order
from announcements.models import Announcements
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy
#THIS IS A NEW COMMENT
# Create your views here.
@login_required
def login_success(request):
    if request.user.profile.user_group == 'store_manager':
        return redirect('order-home')
    else:
        return redirect('parts-home')
    
@login_required
def home(request):
    if request.user.profile.user_group == 'store_manager':
        messages.warning(request, "You do not have permission to access the Engineers Dashboard")
        return redirect('login-success')
    
    announcements = Announcements.objects.filter(visible = True)

    # Get search value from quick search
    search_value = request.GET.get('searchVal')
    
    # If search value is found pass into part list page to filter list of parts
    if search_value:
        return redirect(f"{reverse('parts-list')}?searchVal={search_value}")
    
    # Create empty dictionaries to store past and current orders
    past_orders = []
    current_orders = []

    # Get all orders for current user
    orders = Order.objects.filter(user = request.user).order_by('collection_datetime')

    # Sort orders by status and add to relevent dictonary
    for order in orders:
        if order.status == 'collected':
            past_orders.append(order)
        else:
            current_orders.append(order)

    context = {
        'title': 'Home',
        'announcements': announcements,
        'past_orders': past_orders,
        'current_orders': current_orders,
        'past_orders_count': len(past_orders), # Count number of past orders
        'current_orders_count': len(current_orders) # Count number of current orders
    }
    return render(request, 'parts/home.html', context)

class PartListView(LoginRequiredMixin, ListView):
    model = Part
    context_object_name = 'parts'
    ordering = ['code']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get seach value, if not set set as empty
        search_value = self.request.GET.get('searchVal', '')
        # If search value exists, filter parts where code or name contains search value
        if search_value:
            queryset = queryset.filter(Q(code__icontains=search_value) | Q(name__icontains=search_value))
        return queryset[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search value to context
        context['search_value'] = self.request.GET.get('searchVal', '')
        return context
    
class PartDetailView(LoginRequiredMixin, DetailView):
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
    

class PartCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Part
    fields=['code', 'name', 'num_in_stock', 'low_stock_warning', 'location']

    def get_success_url(self):
        messages.success(self.request, "New Part added successfully!")
        return reverse_lazy('parts-list')
    
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to add a new part")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())
        
class PartUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Part
    fields=['code', 'name', 'low_stock_warning', 'location']


    def get_success_url(self):
        messages.success(self.request, "Part details updated successfully!")
        return reverse('part-detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to update a parts details")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())
        
class PartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Part

    def get_success_url(self):
        messages.success(self.request, "Part deleted")
        return reverse_lazy('parts-list')
    
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to delete a part")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())
        
class LowStockListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'parts/low_stock.html'

    def get_queryset(self):
        all_parts = Part.objects.all()
        # Filter parts to only show those low in stock
        low_stock_parts = [part for part in all_parts if part.is_low_stock()]
        return low_stock_parts
    
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to access the Low Stock page")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())