from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from greenvasadev.settings import BASE_DIR
from main.models import ProductsTable, UserDetails


# Create your views here.

def index(request):
    request.session["login_status"] = False
    login_status = request.session["login_status"]
    return render(request, 'landing.html')


def aboutUs(request):
    return render(request, 'about_us.html')


def rules(request):
    return render(request, 'rules_regulations.html')


def g_sign_up(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
        if request.method == 'POST':
            if request.POST['nPassword1'].strip() == request.POST['nPassword2'].strip():
                user = User(password=make_password(request.POST['nPassword1'].strip()),
                            username=request.POST['nEmail'],
                            email=request.POST['nEmail'],
                            first_name=request.POST['nName'])
                user.save()
                userdetails = UserDetails(user_name=user.username, email=user.email,
                                          mobile_number=request.POST['nPhone'], user_id=user)
                userdetails.save()
                return redirect('main:g_login')
            else:
                context = {
                    'msg': 'Error in the inputs given, kindly make sure that you are using proper details to create user'
                }
                return render(request, 'sign_up.html', context)
        context = {
            'msg': ''
        }
        return render(request, 'sign_up.html', context)


def g_login(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
        if request.method == 'POST':
            Email = request.POST.get('email_address')
            password = request.POST.get('password')

            user = authenticate(request, username=Email, password=password)

            if user is not None:
                login(request, user)
                request.session["login_status"] = True
                request.session["user_email"] = user.email
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                elif user.is_staff == 1:
                    return redirect('main:admin_dashboard')
                else:
                    return redirect('main:seller')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')


def products(request):
    product = ProductsTable.objects.filter(status='APPROVED')
    return render(request, 'products.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def admin_dashboard(request):
    all_pending = ProductsTable.objects.filter(status='WAITING').count()
    all_approved = ProductsTable.objects.filter(status='APPROVED').count()
    all_rejected = ProductsTable.objects.filter(status='REJECTED').count()
    all_sold = ProductsTable.objects.filter(status='SOLD').count()

    return render(request, 'admin_dashboard.html',
                  {'all_sold': all_sold, 'all_approved': all_approved, 'all_pending': all_pending,
                   'all_rejected': all_rejected})


@login_required
def yourProducts(request):
    if request.user.is_authenticated:
        userProducts = ProductsTable.objects.filter(user_id=request.user)
        return render(request, 'yourProducts.html', {'adminProducts': userProducts})
    else:
        return redirect('main:index')


@staff_member_required(login_url='/admin')
def products_admin(request):
    product = ProductsTable.objects.filter(status='WAITING')
    return render(request, 'products_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def products_deleted_admin(request):
    product = ProductsTable.objects.filter(status='REJECTED')
    return render(request, 'products_deleted_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def products_live_admin(request):
    product = ProductsTable.objects.filter(status='APPROVED')
    return render(request, 'live_products_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def products_sold_admin(request):
    product = ProductsTable.objects.filter(status='SOLD')
    return render(request, 'products_sold_details_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


@login_required(login_url='/login')
def product_details(request, product):
    sel_product = ProductsTable.objects.get(product_id=product)
    sellerDetails = UserDetails.objects.get(user_id__email=sel_product.user_id)

    return render(request, 'products_details.html',
                  {'product': sel_product, 'sellerDetails': sellerDetails, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def product_details_admin(request, product):
    sel_product = ProductsTable.objects.get(product_id=product)
    sellerDetails = UserDetails.objects.get(user_id__email=sel_product.user_id)
    message = ''

    if request.method == 'POST' and 'approve' in request.POST:
        productDetails = ProductsTable.objects.get(product_id=request.POST['productID'])
        productDetails.remark = request.POST['productComments']
        productDetails.status = 'APPROVED'
        productDetails.status_updated_on = timezone.now()
        productDetails.save()
        message = "Product Reviewed and approved to be listed"

    if request.method == 'POST' and 'reject' in request.POST:
        productDetails = ProductsTable.objects.get(product_id=request.POST['productID'])
        productDetails.remark = request.POST['productComments']
        productDetails.status = 'REJECTED'
        productDetails.status_updated_on = timezone.now()
        productDetails.save()
        message = "Product Reviewed and approved to be listed"

    if request.method == 'POST' and 'sold' in request.POST:
        productDetails = ProductsTable.objects.get(product_id=request.POST['productID'])
        productDetails.remark = request.POST['productComments']
        productDetails.status = 'SOLD'
        productDetails.status_updated_on = timezone.now()
        productDetails.save()
        message = "Product Reviewed and approved to be listed"

    return render(request, 'products_details_admin.html',
                  {'product': sel_product, 'sellerDetails': sellerDetails, 'message': message, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def product_live_details_admin(request, id):
    product = ProductsTable.objects.get(id=id)
    user_name = product.user_id
    seller_details = UserDetails.objects.get(email=request.user.email)

    if request.method == 'POST' and 'canceled' in request.POST:
        product_Table = ProductsTable()
        product_Table.user_id = product.user_id
        product_Table.product_name = product.product_name
        product_Table.product_description = product.product_description
        product_Table.expected_price = product.expected_price
        product_Table.category = product.category
        product_Table.product_image1 = product.product_image1
        product_Table.product_image2 = product.product_image2
        product_Table.product_image3 = product.product_image3
        product_Table.product_image4 = product.product_image4

        product_Table.save()
        ap_product = ProductsTable(id=product.id)
        ap_product.delete()
        return redirect('main:admin_products')

    return render(request, 'products_live_details_admin.html',
                  {'product': product, 'seller_details': seller_details, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def deleted_product_details_admin(request, id):
    product = ProductsTable.objects.get(id=id)
    user_name = product.user_id
    seller_details = UserDetails.objects.get(email=request.user.email)

    if request.method == 'POST' and 'approved' in request.POST:
        product_Table = ProductsTable()
        product_Table.user_id = product.user_id
        product_Table.product_name = product.product_name
        product_Table.product_description = product.product_description
        product_Table.expected_price = product.expected_price
        product_Table.category = product.category
        product_Table.product_image1 = product.product_image1
        product_Table.product_image2 = product.product_image2
        product_Table.product_image3 = product.product_image3
        product_Table.product_image4 = product.product_image4
        product_Table.remark = request.POST.get("remarks", False)

        product_Table.save()
        ap_product = ProductsTable(id=product.id)
        ap_product.delete()
        return redirect('main:admin_products')

    if request.method == 'POST' and 'deleted' in request.POST:
        product_Table = ProductsTable()
        product_Table.user_id = product.user_id
        product_Table.product_name = product.product_name
        product_Table.product_description = product.product_description
        product_Table.expected_price = product.expected_price
        product_Table.category = product.category
        product_Table.product_image1 = product.product_image1
        product_Table.product_image2 = product.product_image2
        product_Table.product_image3 = product.product_image3
        product_Table.product_image4 = product.product_image4

        product_Table.save()
        dp_product = ProductsTable(id=product.id)
        dp_product.delete()
        return redirect('main:admin_products')

    return render(request, 'deleted_products_details_admin copy.html',
                  {'product': product, 'seller_details': seller_details, 'BASE_DIR': BASE_DIR})


@login_required(login_url='/login')
def productAdded(request, product):
    context = {
        'product': ProductsTable.objects.get(product_id=product),
        'BASE_DIR': BASE_DIR
    }
    return render(request, 'product_added.html', context)


@login_required(login_url='/login')
def g_seller(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            user_id = request.session["user_email"]
            productName = request.POST.get("product_name", False)
            productCategory = request.POST.get("product_category", False)
            productPrice = request.POST.get("product_price", False)
            productDescription = request.POST.get("product_description", False)
            productImage1 = request.FILES.get("pro-image1", False)
            productImage2 = request.FILES.get("pro-image2", False)
            productImage3 = request.FILES.get("pro-image3", False)
            productImage4 = request.FILES.get("pro-image4", False)
            product_id = uuid4()

            product_Table = ProductsTable()
            product_Table.product_id = product_id
            product_Table.user_id = user_id
            product_Table.product_name = productName
            product_Table.category = productCategory
            product_Table.expected_price = productPrice
            product_Table.product_description = productDescription
            product_Table.product_created_on = timezone.now()
            product_Table.product_image1 = productImage1
            product_Table.product_image2 = productImage2
            product_Table.product_image3 = productImage3
            product_Table.product_image4 = productImage4
            product_Table.status = "WAITING"
            product_Table.status_updated_on = timezone.now()
            product_Table.remark = ""

            product_Table.save()

            return redirect('main:success', product_id)
        except:
            context = {
                "error": "Error in adding product, please try after sometime."
            }
            return render(request, 'seller_page.html', context)

    else:
        return render(request, 'seller_page.html')
