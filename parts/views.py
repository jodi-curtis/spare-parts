from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Part
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    context = {
        'title': 'Home'
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

        return redirect('part-detail', pk=current_part.pk)
    

class LowStockListView(ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'parts/low_stock.html'

    def get_queryset(self):
        all_parts = Part.objects.all()
        low_stock_parts = [part for part in all_parts if part.is_low_stock()]
        return low_stock_parts