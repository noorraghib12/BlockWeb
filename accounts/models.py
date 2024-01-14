from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime
from .manager import UserManager
# Create your models here.

def get_user_profile_photo_dir(instance,filename):
    username=instance.user.username
    return f"media/{username}/{filename}"



class User(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=200,unique=True)
    password=models.CharField(max_length=200)
    is_active=models.BooleanField(default=False)
    email_verify_token=models.CharField(max_length=200,default=None)

    REQUIRED_FIELDS=['email']

    objects=UserManager()


    def __str__(self):
        return str([self.email,self.email_verify_token])



class Profile(models.Model):
    credit = models.FloatField()
    address=models.CharField(max_length=500)
    contact=models.CharField(max_length=100)
    profile_photo=models.ImageField(upload_to=get_user_profile_photo_dir,default='media/default/blank-profile-picture.jpg')

def __str__(self):
    return self.user.username
    
