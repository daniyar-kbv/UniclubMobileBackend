from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage

import os
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email(subject, body, to, attachments=None, count=0):
    logger.info(f'Task: Email sending to {to} started')
    if count == 10:
        return False
    try:
        email = EmailMessage(
            subject,
            body,
            from_email=os.environ['EMAIL_HOST_USER'],
            to=[to]
        )
        if attachments:
            for attachment in attachments:
                email.attach_file(attachment)
        email.send()
        logger.info(f'Task: Email sending to {to} finished')
        return True
    except Exception as e:
        logger.info(f'Task: Email sending to {to} failed {print(e) if count == 0 else ""}')
        return send_email(subject, body, to, attachments, count=count+1)
