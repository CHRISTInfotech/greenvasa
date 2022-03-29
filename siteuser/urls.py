from django.urls import path
from siteuser.views import dashboard

urlpatterns = [
    path('dashboard', dashboard, name='dashboard-user'),
]
