from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    name = 'applications'
    verbose_name = '2: Заявки'

    def ready(self):
        from . import signals
