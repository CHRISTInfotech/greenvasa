from itertools import product
from unicodedata import category
from django.db import models

# Create your models here.


class G_Sign_up(models.Model):
    # user_id = 
    product_name = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=False, null=False)
    expected_price = models.CharField(max_length=12,blank=False, null=False)
    product_description = models.CharField(max_length=500, blank=False, null=False)
    product_image = models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        db_table = 'product_table'
