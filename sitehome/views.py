import math
import random
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from settings.appSettings import OTPdigits, address
from siteadmin.models import UserDetails
from sitehome.models import OTPRequest


def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirectUser(request, request.user.email)
        else:
            print(request.POST['login-email'].strip(), request.POST['password-login'].strip())
            user = authenticate(request, username=request.POST['login-email'].strip(),
                                password=request.POST['password-login'].strip())
            print(user)
            if user is not None:
                if user.is_active and len(User.objects.filter(email=request.POST['login-email'].strip())) != 0:
                    login(request, user)
                    return redirectUser(request, request.POST['login-email'].strip())
                else:
                    messages.error(request, 'Your access has been terminated, please contact system administrator!')
                    return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials!')
                return redirect('home')
    else:
        if request.user.is_authenticated:
            return redirectUser(request, request.user.email)
        else:
            return render(request, 'home/index.html')


def redirectUser(request, email):
    userDetails = UserDetails.objects.get(user_id__email=email)
    if userDetails.role == 'ADMIN':
        return redirect('dashboard-admin')
    elif userDetails.role == 'STAFF':
        return redirect('dashboard-staff')
    elif userDetails.role == 'STUDENT':
        return redirect('dashboard-student')
    elif userDetails.role == 'ST.COUNCIL':
        return redirect('dashboard-swo')


# logout the user from the page
def logout_user(request):
    logout(request)
    return redirect('home')


def valEmail(request):
    if request.POST and not request.user.is_authenticated:
        if 'christuniversity.in' in request.POST['emailInput'].strip():
            if len(UserDetails.objects.filter(user_id__email=request.POST['emailInput'].strip())) != 0:
                messages.error(request, 'You have an account existing with EzBus, Try forget password.')
                return redirect('home')
            if len(OTPRequest.objects.filter(email=request.POST['emailInput'].strip())) != 0:
                # otpOLD = OTPRequest.objects.get(email=request.POST['emailInput'].strip())
                # otpOLD.delete()
                messages.warning(request, 'You have requested an OTP earlier, please use the same OTP.')
                return redirect('valOTP', request.POST['emailInput'].strip())
            OTP = ""
            for i in range(6):
                OTP += OTPdigits[math.floor(random.random() * 10)]
            otpReq = OTPRequest(email=request.POST['emailInput'].strip(), otp=OTP, timeStamp=datetime.now())
            otpReq.save()
            subject = 'Welcome to EZBus From CHRIST Lavasa'
            message = 'Hi ' + request.POST['emailInput'].strip() + \
                      ',\n\nWelcom to EzBus. \n\n \
                      Your OTP is : ' + OTP + '\n\nThanks and Regards,\nTEAM EZBus\nCHRIST Infotech'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['emailInput'].strip(), ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'OTP has Sent to your email ID')
            return redirect('valOTP', request.POST['emailInput'].strip())
        else:
            messages.error(request, 'Invalid or unsupported email ID')
            return redirect('valEmail')
    elif request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'home/valEmail.html')


def valOTP(request, email):
    if request.POST:
        if len(OTPRequest.objects.filter(email=email)) != 0 and len(
                UserDetails.objects.filter(user_id__email=email)) == 0:
            if len(OTPRequest.objects.filter(otp=request.POST['pOTP'].strip(),
                                             email=request.POST['vEmail'].strip())) != 0:
                return redirect('register', request.POST['pOTP'].strip(), request.POST['vEmail'].strip())
            else:
                messages.error(request, 'Invalid OTP, Please Try again later')
                return redirect('valOTP', email)
        else:
            return redirect('home')
    else:
        if len(OTPRequest.objects.filter(email=email)) != 0 and len(
                UserDetails.objects.filter(user_id__email=email)) == 0:
            context = {
                'OTPEmail': email
            }
            return render(request, 'home/valOTP.html', context)
        else:
            return redirect('home')


def registerUser(request, otp, email):
    if request.POST:
        print("HEllO", OTPRequest.objects.filter(otp=otp, email=email))
        if len(OTPRequest.objects.filter(otp=otp, email=email)) != 0 and len(User.objects.filter(email=email)) == 0:
            if request.POST['nPassword'].strip() == request.POST['ncPassword'].strip():
                user = User(password=make_password(request.POST['nPassword'].strip()),
                            username=request.POST['nEmail'].strip(),
                            last_name=request.POST['nStudent'].strip(), email=request.POST['nEmail'].strip(), is_staff=False,
                            is_active=True,
                            first_name=request.POST['nStudent'].strip())
                user.save()

                role = 'STUDENT'
                if '@christuniversity.in' in request.POST['nEmail'].strip():
                    role = 'STAFF'

                userDetails = UserDetails(user_id=user,
                                          reg_emp_id=request.POST['nRollNumber'].strip(),
                                          gender=request.POST['nGender'].strip(),
                                          department=request.POST['nDepartment'].strip(),
                                          batch=request.POST['nBatch'].strip(),
                                          course=request.POST['nCourse'].strip(),
                                          phone_no=request.POST['nMobile'].strip(),
                                          address=address, role=role)
                userDetails.save()

                if user.is_active:
                    subject = 'Welcome to EZBus From CHRIST Lavasa'
                    message = 'Hi ' + request.POST['nEmail'].strip() + \
                              ',\n\nWelcome to EzBus.\n' \
                              'You can plan your trips from CHRIST Campus using EZBus bus tip booking app.\n' \
                              'Thanks and Regards,\nTEAM EZBus\nCHRIST Infotech'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['nEmail'].strip(), ]
                    send_mail(subject, message, email_from, recipient_list)

                    login(request, user)
                    messages.success(request, 'Thanks you for registering with EZBus')
                    return redirectUser(request, request.POST['nEmail'].strip())
                else:
                    messages.error(request, 'Your access has been terminated, please contact system administrator!')
                    return redirect('home')
            else:
                messages.error(request, "Passwords doesn't match")
                return redirect(request, otp, email)
        else:
            messages.error(request, 'Invalid Request, Please Try again later')
            return redirect('home')
    else:
        if len(OTPRequest.objects.filter(otp=otp, email=email)) != 0:
            context = {
                'departments': appSettings.departments,
                'courses': appSettings.courses,
                'batch': appSettings.batch,
                'gender': appSettings.gender,
                'email': email,
                'otp': otp,
            }
            return render(request, 'home/register.html', context)
        else:
            messages.error(request, 'Invalid Request, Please Try again later')
            return redirect('home')


def faq(request):
    return render(request, 'home/faq.html')


def demo(request):
    return render(request, 'home/demo.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'home/password_reset.html'
    email_template_name = 'email/password_reset_email.html'
    subject = 'EZBus - Registration/Login App Password Reset'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


def error_404_view(request, exception):
    return render(request, 'home/error_404.html')
