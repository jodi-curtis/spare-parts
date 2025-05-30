from django.shortcuts import render, redirect
from django.views.generic import DetailView
from . models import Basket, BasketItem
from parts.models import Part
from orders.models import Order, OrderItem
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login


# Create your views here.
class BasketDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Basket
    template_name = 'basket/basket.html'
    context_object_name = 'basket'

    def get_object(self, queryset=None):
        # Fetch or create a basket for the logged-in user
        basket, created = Basket.objects.get_or_create(user=self.request.user)
        return basket
    
    def post(self, request, *args, **kwargs):
        basket = self.get_object()

        #Remove action
        if 'remove_item_id' in request.POST:
            #Get item id
            item_id = request.POST.get('remove_item_id')
            #Get basket item
            item = BasketItem.objects.get(id=item_id, basket=basket)
            
            #Get quantity of parts which were in basket 
            part_qty = item.quantity

            #Delete Item from users basket
            item.delete()

            #Update part to add quantity back into stock 
            part = Part.objects.get(id=item.part.id)
            part.num_in_stock += part_qty
            part.save()

            messages.success(request, f"{item.part.name} removed from basket")

        if 'collection_datetime' in request.POST:
            #Get collection date and time set
            collection = request.POST.get('collection_datetime')

            #Create Order
            order = Order.objects.create(
                user=request.user,
                collection_datetime = collection
            )

            #Add items from basket to order
            for basket_item in basket.items.all():
                OrderItem.objects.create(
                    order=order,
                    part=basket_item.part,
                    quantity=basket_item.quantity
                )

            #Remove items from user basket
            basket.items.all().delete()

            messages.success(request, f"Order placed.. keep track of your orders on the dashboard")
        #Redirect to page to refresh basket
        return redirect('basket-home')
    
    def test_func(self):
        return self.request.user.profile.user_group == 'engineer'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to access the Basket page")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())