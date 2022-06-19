from django.shortcuts import render,redirect
from .models import Product_List
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login')
def productAdded(request):
    # request.session["login_status"]=False
    # login_status = request.session["login_status"]
    # if login_status:    
    return render(request,'product_added.html')
    # else:
    #     return redirect('/products/')

@login_required(login_url='/login')
def g_seller(request):
    # login_status = request.session["login_status"]
    # print(request.session["user_name"])
    # print(request.session["user_email"])

    # if login_status == True:
    #     # print(request.session["user_email"])
    if request.method == 'POST':
        user_id = request.session["user_email"]
        productName = request.POST.get("product_name", False)
        productCategory = request.POST.get("product_category", False)
        productPrice = request.POST.get("product_price", False)
        productDescription = request.POST.get("product_description", False)
        productImage1 = request.FILES.get("pro-image1", False)
        productImage2 = request.FILES.get("pro-image2", False)
        productImage3 = request.FILES.get("pro-image3", False)
        productImage4 = request.FILES.get("pro-image4", False)
        # print(productName)
        # print(productImage1)
        # print(productImage2)
        # print(productImage3)
        # print(productImage4)

        product_Table = Product_List()
        product_Table.user_id = user_id
        product_Table.product_name = productName
        product_Table.product_description = productDescription
        product_Table.expected_price = productPrice
        product_Table.category = productCategory
        product_Table.product_image1 = productImage1
        product_Table.product_image2 = productImage2
        product_Table.product_image3 = productImage3
        product_Table.product_image4 = productImage4

        product_Table.save()

        return redirect('/g/seller/submitted')

    return render(request,'seller_page.html')

@login_required(login_url='/login')
def g_app_seller(request):
    # login_status = request.session["login_status"]
    # print(request.session["user_name"])
    # print(request.session["user_email"])

    # if login_status == True:
    #     # print(request.session["user_email"])
    if request.method == 'POST':
        user_id = request.session["user_email"]
        productName = request.POST.get("product_name", False)
        productCategory = request.POST.get("product_category", False)
        productPrice = request.POST.get("product_price", False)
        productDescription = request.POST.get("product_description", False)
        productImage1 = request.FILES.get("pro-image1", False)
        productImage2 = request.FILES.get("pro-image2", False)
        productImage3 = request.FILES.get("pro-image3", False)
        productImage4 = request.FILES.get("pro-image4", False)
        # print(productName)
        # print(productImage1)
        # print(productImage2)
        # print(productImage3)
        # print(productImage4)

        product_Table = Product_List()
        product_Table.user_id = user_id
        product_Table.product_name = productName
        product_Table.product_description = productDescription
        product_Table.expected_price = productPrice
        product_Table.category = productCategory
        product_Table.product_image1 = productImage1
        product_Table.product_image2 = productImage2
        product_Table.product_image3 = productImage3
        product_Table.product_image4 = productImage4

        product_Table.save()

        return redirect('/g/seller/submitted')

    return render(request,'seller_page.html')



