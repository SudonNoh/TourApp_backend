from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile
from users.models import User


@receiver(post_save, sender=User)
def create_related_pofile(sender, instance, created, *args, **kwargs):
    if isinstance and created:
        instance.profile = Profile.objects.create(
            user=instance,
            username=instance.email
        )