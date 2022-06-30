from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from greenvasadev.settings import BASE_DIR
from main.forms import CreateUserForm
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
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                Name = request.POST["username"]
                Email = request.POST["email"]
                Mobile_Number = request.POST["phone"]
                # Password = request.POST.get("confirm_password", False)

                sign_up_data = UserDetails()
                sign_up_data.user_name = Name
                sign_up_data.email = Email
                sign_up_data.mobile_number = Mobile_Number
                # sign_up_data.password = Password
                sign_up_data.save()

                return redirect('sign_up_in:g_login')

        context = {'form': form}
        return render(request, 'sign_up.html', context)


def g_login(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
        if request.method == 'POST':
            # Email = request.POST.get('email_address')
            Email = request.POST.get('email_address')
            password = request.POST.get('password')

            print(Email)
            print(password)

            user = authenticate(request, username=Email, password=password)

            if user is not None:
                print("Login success")
                login(request, user)
                request.session["login_status"] = True
                request.session["user_email"] = user.email
                print(request.session["user_email"])
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                elif user.is_staff == 1:
                    return redirect('main:admin_dashboard')
                else:
                    return redirect('seller:seller')
            else:
                print('Login is not success')
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')

def products(request):
    product = ProductsTable.objects.all()
    print(type(product))
    print(len(product))
    print(BASE_DIR)
    # print(product[0].product_image1)
    # print(product[0].id)
    # print(product[1].id)
    return render(request, 'products.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def admin_dashboard(request):
    product = ProductsTable.objects.all()
    approved_products = ProductsTable.objects.all()
    deleted_prod = ProductsTable.objects.all()
    all_pending = len(product)
    all_approved = len(approved_products)
    all_deleted_prod = len(deleted_prod)

    return render(request, 'admin_dashboard.html',
                  {'products': product, 'all_approved': all_approved, 'all_pending': all_pending,
                   'all_deleted_prod': all_deleted_prod, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def products_admin(request):
    product = ProductsTable.objects.all()
    return render(request, 'products_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def products_deleted_admin(request):
    product = ProductsTable.objects.all()
    print(type(product))
    print(len(product))
    print(BASE_DIR)
    # print(product[0].product_image1)
    # print(product[0].id)
    # print(product[1].id)
    return render(request, 'products_deleted_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def products_live_admin(request):
    product = ProductsTable.objects.all()
    print(type(product))
    print(len(product))
    print(BASE_DIR)

    return render(request, 'live_products_admin.html', {'products': product, 'BASE_DIR': BASE_DIR})


# @staff_member_required(login_url='/admin')
def product_details(request, id):
    product = ProductsTable.objects.get(id=id)
    user_name = product.user_id
    seller_details = UserDetails.objects.get(email=request.user.email)

    return render(request, 'products_details.html',
                  {'product': product, 'seller_details': seller_details, 'BASE_DIR': BASE_DIR})


@staff_member_required(login_url='/admin')
def product_details_admin(request, id):
    product = ProductsTable.objects.get(id=id)
    user_name = product.user_id
    seller_details = UserDetails.objects.get(email=user_name)

    if request.method == 'POST' and 'approved' in request.POST:
        # if  'approved' in self.data:
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

    if request.method == 'POST' and 'canceled' in request.POST:
        # if 'canceled' in self.data:
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

    return render(request, 'products_details_admin.html',
                  {'product': product, 'seller_details': seller_details, 'BASE_DIR': BASE_DIR})


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
