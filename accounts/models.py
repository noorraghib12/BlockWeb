from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime
from .manager import UserManager
# Create your models here.





class User(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=200,unique=True)
    password=models.CharField(max_length=200,required=True)
    is_active=models.BooleanField(default=False)
    email_verify_token=models.CharField(default=None)

    REQUIRED_FIELDS=['email']

    objects=UserManager()


    def __str__(self):
        return self.user.email


