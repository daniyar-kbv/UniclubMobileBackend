from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Course, WeekDay

import constants


@receiver(post_save, sender=Course)
def course_saved(sender, instance, created, **kwargs):
    if created:
        for weekday in constants.WEEKDAYS:
            WeekDay.objects.create(course=instance, day=weekday[0])
