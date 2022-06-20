from itertools import product
from unicodedata import category
from django.db import models

# Create your models here.

def user_directory_path2(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}/{1}/{2}'.format("files",instance.user_id,filename)


class Approved_Product_List(models.Model):
    user_id = models.CharField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=False, null=False)
    expected_price = models.CharField(max_length=12,blank=False, null=False)
    product_description = models.CharField(max_length=1500, blank=False, null=False)
    product_image1 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image2 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image3 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image4 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    remark = models.CharField(max_length=100, blank=False, null=True)
    class Meta:
        db_table = 'approved_product_table'

class Deleted_Product_List(models.Model):
    user_id = models.CharField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=False, null=False)
    expected_price = models.CharField(max_length=12,blank=False, null=False)
    product_description = models.CharField(max_length=1500, blank=False, null=False)
    product_image1 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image2 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image3 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image4 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    remark = models.CharField(max_length=100, blank=False, null=True)
    class Meta:
        db_table = 'deleted_product_table'

class Product_List(models.Model):
    user_id = models.CharField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=False, null=False)
    expected_price = models.CharField(max_length=12,blank=False, null=False)
    product_description = models.CharField(max_length=1500, blank=False, null=False)
    product_image1 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image2 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image3 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image4 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    class Meta:
        db_table = 'product_table'
