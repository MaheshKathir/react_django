from django.db import models


# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
