import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniclub_mobile.settings')

app = Celery('uniclub_mobile')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()