from email.policy import default
from tkinter.tix import Tree
from django.db import models
from django.core.files.storage import FileSystemStorage

from core.models import TimestampedModel


fs = FileSystemStorage(location='/media')


def upload_to(instance, filename):
    return 'profiles/%s/%s' % (instance.user.email, filename)


class Profile(TimestampedModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    username = models.CharField(max_length=128, unique=True)
    birth = models.DateField(blank=True, null=True)
    profile_img = models.ImageField(
        storage=fs, upload_to=upload_to, blank=True,
        )
    introduce = models.TextField(blank=True)

    def __str__(self):
        return self.user.email
