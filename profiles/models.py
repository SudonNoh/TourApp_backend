from datetime import datetime
from email.policy import default
from django.db import models
from django.core.files.storage import FileSystemStorage

from core.models import TimestampedModel

# fileststem에 location과 base_url을 설정해주면 settings의
# MEDIA_ROOT와 MEDIA_URL들은 관계없이 기본 os로 경로가 설정된다.
# 설정을 안할 경우 settings의 MEDIA_ROOT와 MEDIA_URL을 따른다.
fs = FileSystemStorage()


def upload_to(instance, filename):
    date_now = datetime.strftime(datetime.now(), '%Y/%m/%d')
    dir_path =  'images/profiles/'+str(instance.user.id)+"/"+date_now
    return '%s/%s' % (dir_path, filename)


class Profile(TimestampedModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    username = models.CharField(max_length=128, unique=True)
    birth = models.DateField(blank=True, null=True)
    profile_img = models.ImageField(
        storage=fs, upload_to=upload_to, blank=True, default='images/init/ryan.jpg'
    )
    introduce = models.TextField(blank=True)

    def __str__(self):
        return self.user.id
