from django.shortcuts import render,redirect

# Create your views here.


def g_seller(request):
    login_status = request.session["login_status"]
    # print(request.session["user_name"])
    # print(request.session["user_email"])

    if login_status == True:
        print(request.session["user_email"])
        return render(request,'seller_page.html')
    else:
        return redirect('sign_up_in:g_login')