from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    username = models.CharField(unique=True, max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.jpg')
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_loggedin = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']