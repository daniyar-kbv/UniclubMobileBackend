from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from main.models import LessonTime, Course
from other.models import TimestampModel


class PartnershipApplication(TimestampModel):
    class Meta:
        verbose_name = "Заявки на партнерство"
        verbose_name_plural = "Заявки на партнерство"

    name = models.CharField("Имя", max_length=256)
    company_name = models.CharField("Название компании", max_length=256, null=True, blank=False)
    email = models.EmailField("e-mail", null=True, blank=True)
    mobile_phone = PhoneNumberField("Мобильный телефон", null=True, blank=True)

    def __str__(self):
        return f"{self.name}({self.company_name})"


class BookingApplication(TimestampModel):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    phone_number = PhoneNumberField('Номер телефона')
    email = models.EmailField('Email')

    class Meta:
        verbose_name = 'Заявка на бронирование'
        verbose_name_plural = 'Заявки на бронирование'

    def __str__(self):
        return f'({self.id}) {self.first_name} {self.last_name}'


class CourseBooking(TimestampModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='course_bookings'
    )
    lesson_times = models.ManyToManyField(
        LessonTime,
        verbose_name='Время занятий',
        related_name='course_bookings'
    )
    booking_application = models.ForeignKey(
        BookingApplication,
        on_delete=models.CASCADE,
        verbose_name='Заявка на бронирование',
        related_name='course_booking'
    )

    class Meta:
        verbose_name = 'Бронирование курса'
        verbose_name_plural = 'Бронирования курсов'

    def __str__(self):
        return f'({self.id}) {self.course}'
