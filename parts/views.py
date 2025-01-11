from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Part
from django.views.generic import ListView
from django.db.models import Q

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