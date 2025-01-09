from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Part


# Create your views here.
@login_required
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'parts/home.html', context)

@login_required
def parts(request):
    context = {
        'title': 'Spare Parts',
        'parts': Part.objects.all() 
    }
    return render(request, 'parts/parts.html', context)