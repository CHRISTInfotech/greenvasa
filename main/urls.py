from django.urls import path

from . import views

app_name='main'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('about-us/', views.aboutUs, name='aboutUs'),
    path('products_details/<int:id>', views.product_details),
    path('admin/products/', views.products_admin, name='admin_products'),
    path('admin/products_details/<int:id>', views.product_details_admin),
]