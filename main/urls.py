from django.urls import path

from . import views

app_name='main'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('about-us/', views.aboutUs, name='aboutUs'),
    path('products_details/<int:id>', views.product_details),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.products_admin, name='admin_products'),
    path('admin/live_products/', views.products_live_admin, name='admin_live_products'),
    path('admin/deleted_products/', views.products_deleted_admin, name='admin_deleted_products'),
    path('admin/products_details/<int:id>', views.product_details_admin),
    path('admin/live_products_details/<int:id>', views.product_live_details_admin),
    path('admin/deleted_products_details/<int:id>', views.deleted_product_details_admin),
]