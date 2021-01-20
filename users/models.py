from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='profile'
    )
    website_url = models.URLField('Адрес вебсайта', null=True, blank=True)
    club_name = models.CharField('Название клуба', max_length=100, null=True, blank=True)
    about_club = models.TextField('О клубе', null=True, blank=True)
    contacts = models.TextField('Контактная информация', null=True, blank=True)
    club_is_active = models.BooleanField('Клуб активен', default=False, null=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user}'
