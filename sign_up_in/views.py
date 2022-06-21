from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import G_Sign_up


from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm
# Create your views here.

# def g_login(request):
#     return render(request,'login.html')

# def g_sign_up(request):
#     if request.method == 'POST':
#         Name = request.POST.get("name", False)
#         Email = request.POST.get("email_address", False)
#         Mobile_Number = request.POST.get("mobile_number", False)
#         Password = request.POST.get("confirm_password", False)

#         sign_up_data = G_Sign_up()
#         sign_up_data.user_name = Name
#         sign_up_data.email = Email
#         sign_up_data.mobile_number = Mobile_Number
#         sign_up_data.password = Password
#         sign_up_data.save()

#         return redirect("sign_up_in:g_login")


#     return render(request,'sign_up.html')


# def g_login(request):
#     print('View is requested')
#     if request.method == "POST":
#         Email = request.POST.get("email_address")
#         Password = request.POST.get("password")

#         print(Email)
#         print(Password)
#         # request.session["user_email"]=Email
#         try:
#             user = G_Sign_up.objects.get(email=Email,password = Password)
#             # user = authenticate(email=Email,password = Password)
#             print(user)
#             if user is not None:
#                 print('User is there')
#                 # request.session["user_name"]=user['name']
#                 request.session["user_email"]=Email
#                 request.session["login_status"]=True

#                 return redirect('main:products')
#             # else:
#             #     print("User doesnot exist")
#             #     #return redirect('sellersignin')
#             #     return HttpResponse("User doesnot exist.")
#         except Exception as identifier:
#             request.session["login_status"]=False
#             #return redirect('sellersignin')
#             return HttpResponse("Email or Password is incorrect.")
# 			# return messages.info(request, 'Username OR password is incorrect')
#     else:
#         return render(request,'login.html')


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

				sign_up_data = G_Sign_up()
				sign_up_data.user_name = Name
				sign_up_data.email = Email
				sign_up_data.mobile_number = Mobile_Number
				# sign_up_data.password = Password
				sign_up_data.save()

				return redirect('sign_up_in:g_login')
			

		context = {'form':form}
		return render(request, 'sign_up.html', context)


def g_login(request):
	if request.user.is_authenticated:
		return redirect('/products')
	else:
		if request.method == 'POST':
			# Email = request.POST.get('email_address')
			Email = request.POST.get('email_address')
			password =request.POST.get('password')


			print(Email)
			print(password)

			user = authenticate(request, username=Email, password=password)

			if user is not None:
				print("Login success")
				login(request, user)
				request.session["login_status"]=True
				request.session["user_email"]=user.email
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