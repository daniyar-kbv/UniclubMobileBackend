from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '1: Пользователи'

    def ready(self):
        from . import signals

