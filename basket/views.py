from django.shortcuts import render, redirect
from django.views.generic import DetailView
from . models import Basket, BasketItem
from parts.models import Part
from django.contrib import messages


# Create your views here.
class BasketDetailView(DetailView):
    model = Basket
    template_name = 'basket/basket.html'
    context_object_name = 'basket'

    def get_object(self, queryset=None):
        # Fetch or create a basket for the logged-in user
        basket, created = Basket.objects.get_or_create(user=self.request.user)
        return basket
    
    def post(self, request, *args, **kwargs):
        basket = self.get_object()

        # Handle remove action
        if 'remove_item_id' in request.POST:
            # Get item id
            item_id = request.POST.get('remove_item_id')
            # Get item from users basket
            item = BasketItem.objects.get(id=item_id, basket=basket)
            
            # Get quantity of parts which were in basket 
            part_qty = item.quantity

            # Delete Item from users basket
            item.delete()

            # Update part to add quantity back into stock 
            part = Part.objects.get(id=item.part.id)
            part.num_in_stock += part_qty
            part.save()

            messages.success(request, f"{item.part.name} removed from basket")

        # Redirect to page to refresh basket
        return redirect('basket-home')