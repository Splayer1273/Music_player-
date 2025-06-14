from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.username
    
