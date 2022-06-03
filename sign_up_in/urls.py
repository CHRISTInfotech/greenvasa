from django.urls import path

from . import views

app_name='sign_up_in'

urlpatterns = [
    path('login/', views.g_login, name='g_login'),
    path('sign_up/', views.g_sign_up, name='g_sign_up'),
    
]