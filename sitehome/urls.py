from django.urls import path
from sitehome.views import index, registerUser, faq, demo, logout_user, ResetPasswordView,valEmail,valOTP
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='home'),
    path('faq', faq, name='faq'),
    path('demo', demo, name='demo'),
    path('logout', logout_user, name='logout'),
    path('valEmail', valEmail, name='valEmail'),
    path('valOTP/<str:email>', valOTP, name='valOTP'),
    path('register/<str:otp>/<str:email>', registerUser, name='register'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),
         name='password_reset_complete'),
]
