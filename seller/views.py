from django.shortcuts import render

# Create your views here.


def g_seller(request):
    return render(request,'seller_page.html')