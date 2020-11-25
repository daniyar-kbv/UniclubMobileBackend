from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from PIL import Image, ExifTags

from other.models import AgeGroup, AttendanceType, AdministrativeDivision, GradeTypeGroup, GradeType, TimestampModel
from utils import general

import constants


class Course(TimestampModel):
    name = models.CharField('Название', max_length=500)
    description = models.TextField('Описание')
    from_age = models.PositiveSmallIntegerField('Возраст от', null=True)
    to_age = models.PositiveSmallIntegerField('Возраст до', null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='courses',
        null=True
    )
    attendance_type = models.ForeignKey(
        AttendanceType,
        on_delete=models.SET_NULL,
        verbose_name='Вид посещения',
        related_name='courses',
        null=True
    )
    administrative_division = models.ForeignKey(
        AdministrativeDivision,
        on_delete=models.SET_NULL,
        verbose_name='Административное деление',
        related_name='courses',
        null=True
    )
    grade_group = models.ForeignKey(
        GradeTypeGroup,
        on_delete=models.SET_NULL,
        verbose_name='Группа занятий',
        related_name='courses',
        null=True
    )
    grade_type = models.ForeignKey(
        GradeType,
        on_delete=models.SET_NULL,
        verbose_name='Вид занятия',
        related_name='courses',
        null=True
    )

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['-created_at']

    def __str__(self):
        return f'({self.id}) {self.name}'

    def clean(self):
        if self.from_age >= self.to_age:
            raise ValidationError("Возраст от должен быть меньше возраста до")


class CourseImage(TimestampModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='images'
    )
    image = models.ImageField(
        "Изображение",
        upload_to="course_images/",
        null=True
    )
    is_main = models.BooleanField('Основное', default=False)

    class Meta:
        verbose_name = 'Фото курса'
        verbose_name_plural = 'Фото курсов'
        ordering = ['is_main', 'id']

    def __str__(self):
        return f'({self.id}) {self.course}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(CourseImage, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(CourseImage, self).save(*args, **kwargs)

        if self.image:
            image = Image.open(self.image.path)

            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            if image._getexif():
                exif = dict(image._getexif().items())

                if exif.get(orientation) == 3:
                    image = image.rotate(180, expand=True)
                elif exif.get(orientation) == 6:
                    image = image.rotate(270, expand=True)
                elif exif.get(orientation) == 8:
                    image = image.rotate(90, expand=True)

            image.save(self.image.path, quality=50, optimize=True)


class WeekDay(TimestampModel):
    day = models.PositiveSmallIntegerField(
        verbose_name="День недели",
        choices=constants.WEEKDAYS
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='weekdays',
    )

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'
        ordering = ['day']

    def __str__(self):
        return f'({self.id}) {general.get_value_from_choices(constants.WEEKDAYS, self.day)}'


class LessonTime(TimestampModel):
    weekday = models.ForeignKey(
        WeekDay,
        on_delete=models.CASCADE,
        verbose_name='День недели',
        related_name='lesson_times'
    )
    from_time = models.TimeField('От')
    to_time = models.TimeField('До')

    class Meta:
        verbose_name = 'Время занятия'
        verbose_name_plural = 'Время занятий'
        ordering = ['weekday', 'from_time', 'to_time']

    def __str__(self):
        return f'({self.id}) {self.from_time}-{self.to_time}'

    def clean(self):
        if self.from_time >= self.to_time:
            raise ValidationError('Время начала должно быть раньше чем время конца')
