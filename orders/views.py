from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.views.generic import ListView

# Create your views here.

def home(request):
    return HttpResponse('<h1>Orders Home</h1>')

class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
