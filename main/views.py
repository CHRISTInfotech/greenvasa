from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'landing.html')


def products(request):
    return render(request,'products.html')