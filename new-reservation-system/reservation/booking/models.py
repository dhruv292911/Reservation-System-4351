from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime, date

# Create your models here.
class registeredUser(models.Model):
    username = models.CharField(max_length = 15, primary_key = True)
    password = models.CharField(max_length = 20)
    mailing_address = models.TextField(default = "Default Address")
    billing_address = models.TextField(default = "Default Address")
    pref_payment_method = models.CharField(max_length = 20) 
    cc_num = models.IntegerField(default = 1111111111111111)
    points = models.IntegerField(default = 0)


    def _str_(self):
        return self 


class Date(models.Model):
    reservation_date = models.DateField(auto_now_add=False, auto_now=False)

class Table(models.Model):
    capacity = models.IntegerField(default = 1)
    dates = models.ManyToManyField(Date , blank = True)


class Reservation(models.Model):
    name = models.CharField(max_length = 15, default = "no data")
    party_size = models.IntegerField(default = 1)
    email = models.EmailField(max_length = 254, default= "customer_default@gmail.com")
    reservation_phone = models.CharField(max_length = 10, null= True)


    tables = models.ManyToManyField(Table)
    dates = models.ForeignKey(Date, on_delete=models.CASCADE , default = 1)

    