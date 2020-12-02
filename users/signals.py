from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile
from utils import general

import constants


@receiver(post_save, sender=User)
def course_saved(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
