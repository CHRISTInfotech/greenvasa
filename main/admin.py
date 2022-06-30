from django.contrib import admin

# Register your models here.
from main.models import ProductsTable, UserDetails

admin.site.register(ProductsTable)
admin.site.register(UserDetails)