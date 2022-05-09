from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class user_detail(models.Model):
    
    name=models.CharField(max_length=100,null=True)
    auth_token = models.CharField(max_length =100)
    dob=models.DateField()
    email=models.EmailField(primary_key=True)
    gender =models.CharField(max_length=100)
    height=models.DecimalField(decimal_places=2,max_digits=5)
    weight =models.DecimalField(decimal_places=2,max_digits=5)
    is_verified =models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)
    adult = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_adult(self):
        import datetime
        from dateutil import parser
        if (datetime.datetime.today() - parser.parse(self.dob)) > datetime.timedelta(days=18*365):
            self.adult = True

    def save(self, *args, **kwargs):
        self.is_adult()
        super(user_detail, self).save(*args, **kwargs)

class user_login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100,null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    email=models.EmailField(primary_key=True)


    def __str__(self):
        return self.username
    
