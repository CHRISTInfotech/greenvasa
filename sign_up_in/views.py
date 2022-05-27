from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import G_Sign_up

# Create your views here.

# def g_login(request):
#     return render(request,'login.html')

def g_sign_up(request):
    if request.method == 'POST':
        Name = request.POST.get("name", False)
        Email = request.POST.get("email_address", False)
        Mobile_Number = request.POST.get("mobile_number", False)
        Password = request.POST.get("confirm_password", False)

        sign_up_data = G_Sign_up()
        sign_up_data.user_name = Name
        sign_up_data.email = Email
        sign_up_data.mobile_number = Mobile_Number
        sign_up_data.password = Password
        sign_up_data.save()

        return redirect("sign_up_in:g_login")


    return render(request,'sign_up.html')


def g_login(request):
    print('View is requested')
    if request.method == "POST":
        Email = request.POST.get("email_address")
        Password = request.POST.get("password")

        print(Email)
        print(Password)

        try:
            user = G_Sign_up.objects.get(email=Email,password = Password)
            if user is not None:

                return redirect('main:products')
            # else:
            #     print("User doesnot exist")
            #     #return redirect('sellersignin')
            #     return HttpResponse("User doesnot exist.")
        except Exception as identifier:
            #return redirect('sellersignin')
            return HttpResponse("Email or Password is incorrect.")
    else:
        return render(request,'login.html')