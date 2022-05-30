from django.http import HttpResponse
from django.shortcuts import render

from greenvasadev.settings import BASE_DIR

from seller.models import Product_List

# Create your views here.

def index(request):
    request.session["login_status"]=False
    return render(request,'landing.html')


def products(request):
    product = Product_List.objects.all()
    print(type(product))
    print(len(product))
    print(BASE_DIR)
    print(product[0].product_image1)
    print(product[0].id)
    print(product[1].id)
    return render(request,'products.html', {'products': product, 'BASE_DIR':BASE_DIR})