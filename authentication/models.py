import jwt
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core.models import TimestampedModel
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, TimestampedModel, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=20, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    birth = models.DateField(blank=True)
    type = models.CharField(
        max_length=10,
        choices=(('inApp', 'inApp'), ('naver', 'naver'), ('kakao', 'kakao'))
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'mobile',
        'type'
    ]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self) -> str:
        dt = datetime.now() + timedelta(days=1)
        
        token = jwt.encode({
            'id':self.pk,
            'exp':dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token