from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name='seller'

urlpatterns = [
    path('seller/', views.g_seller, name='seller'),   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)