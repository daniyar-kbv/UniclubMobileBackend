from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Course, WeekDay, CourseImage
from utils import general

import constants


@receiver(post_save, sender=Course)
def course_saved(sender, instance, created, **kwargs):
    if created:
        for weekday in constants.WEEKDAYS:
            WeekDay.objects.create(course=instance, day=weekday[0])


@receiver(pre_delete, sender=CourseImage)
def course_image_pre_delete(sender, instance, created=True, **kwargs):
    if instance.image:
        general.delete_file(instance.image)
