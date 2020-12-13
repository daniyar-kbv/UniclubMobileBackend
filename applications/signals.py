from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from main.tasks import send_email
from .models import BookingApplication, PartnershipApplication
from utils import general

import constants


@receiver(post_save, sender=PartnershipApplication)
def partnership_application_saved(sender, instance, created, **kwargs):
    print('asd')
    if created:
        send_email.delay(
            'Новая заявка на партнерство',
            f"""Заявка на партнераство #{instance.id}
            
Имя: {instance.name}
Название компании: {instance.company_name}
Почта: {instance.email}
Номер телефона: {instance.mobile_phone}""",
            constants.APPLICATIONS_EMAIL
        )


@receiver(post_save, sender=BookingApplication)
def booking_application_saved(sender, instance, created=True, **kwargs):
    attrs_needed = ['_created']
    if all(hasattr(instance, attr) for attr in attrs_needed):
        if instance._created:
            send_email.delay(
                'Новая заявка на бронирование',
                f"""Заявка на бронирование #{instance.id}
                
Имя: {instance.first_name} {instance.last_name}
Почта: {instance.email}
Номер телефона: {instance.phone_number}""",
                constants.APPLICATIONS_EMAIL
            )
            for user in list(set(map(lambda booking: booking.course.user, instance.course_booking.all()))):
                if user.email:
                    send_email.delay(
                        'Новая заявка на бронирование',
                        f"""Заявка на бронирование #{instance.id}
                        
Имя: {instance.first_name} {instance.last_name}""",
                        user.email
                    )
