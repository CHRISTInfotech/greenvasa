from django.db import models

# Create your models here.
class OTPRequest(models.Model):
    email = models.CharField(max_length=150)
    otp = models.CharField(max_length=6)
    timeStamp = models.DateTimeField()