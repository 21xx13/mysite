from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class UserData(models.Model):
    username = models.CharField(max_length=70)
    password = models.CharField(max_length=100)

class Note(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()

