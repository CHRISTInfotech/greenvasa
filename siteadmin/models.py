from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class UserDetails(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_emp_id = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    department = models.CharField(max_length=250)
    batch = models.CharField(max_length=100)
    course = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=15)
    address = models.CharField(max_length=250,
                               default="CHRIST (Deemed to be University), Pune Lavasa Campus, Central Block, Lavasa, Pune, Maharashtra,412112")
    role = models.CharField(max_length=10)

    def __str__(self):
        return self.user_id.__str__()
