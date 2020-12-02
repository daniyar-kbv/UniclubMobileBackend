from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='profile'
    )
    tg_username = models.CharField('Имя пользователя в телеграме', max_length=100, null=True, blank=True)
    website_url = models.URLField('Адрес вебсайта', null=True, blank=True)
    club_name = models.CharField('Название клуба', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'({self.id}) {self.user}'
