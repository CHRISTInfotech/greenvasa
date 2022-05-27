from django.db import models

# Create your models here.


class G_Sign_up(models.Model):
    user_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    mobile_number = models.CharField(max_length=12,blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        db_table = 'registration'


