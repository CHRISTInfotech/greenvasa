from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


def user_directory_path2(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return '{0}/{1}/{2}'.format("files", instance.user_id, filename)


class UserDetails(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    mobile_number = models.CharField(max_length=12, blank=False, null=False)

    class Meta:
        db_table = 'registration'

    def __str__(self):
        return self.user_name


class ProductsTable(models.Model):
    product_id = models.CharField(max_length=255, blank=False, null=False)
    user_id = models.CharField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=False, null=False)
    expected_price = models.CharField(max_length=12, blank=False, null=False)
    product_description = models.CharField(max_length=1500, blank=False, null=False)
    product_created_on = models.DateTimeField(default=timezone.now)
    product_image1 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image2 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image3 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    product_image4 = models.FileField(upload_to=user_directory_path2, null=True, verbose_name="")
    # PRODUCT STATUS: WAITING, APPROVED, REJECTED, SOLD
    status = models.CharField(max_length=50, blank=False, null=True)
    status_updated_on = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=100, blank=False, null=True)

    class Meta:
        db_table = 'product_table'

    def __str__(self):
        return self.product_id