from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Part
from django.db.models import Q

# Create your views here.
@login_required
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'parts/home.html', context)

@login_required
def parts(request):
    #Get search value from search bar
    search_value = request.GET.get('searchVal','')
    #If search value is set
    if search_value:
        #Filter parts list where code or name contains the search value
        parts = Part.objects.filter(Q(code__icontains=search_value) | Q(name__icontains=search_value))
    #If no search value set
    else:
        #Get all parts
        parts = Part.objects.all()
    
    context = {
        'title': 'Spare Parts',
        'parts': parts,
        'search_value': search_value 
    }
    return render(request, 'parts/parts.html', context)