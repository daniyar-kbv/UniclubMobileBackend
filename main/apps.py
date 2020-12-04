from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = '1: Основное'

    def ready(self):
        from . import signals
