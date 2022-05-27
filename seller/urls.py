from django.urls import path

from . import views

app_name='seller'

urlpatterns = [
    path('seller/', views.g_seller, name='seller'),   
]