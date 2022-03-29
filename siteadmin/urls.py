from django.urls import path
from siteadmin.views import dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard-admin'),
]
