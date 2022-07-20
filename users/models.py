import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from core.models import TimestampedModel


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = [
        'mobile',
    ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
