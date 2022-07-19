from django.db import models


# Create your models here.
class Profile(models.Model):
    
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    
    username = models.CharField(max_length=20, unique=True)
    profile_img = models.ImageField(default='media/sample/img/man_img', upload_to=)
    introduce = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
    
