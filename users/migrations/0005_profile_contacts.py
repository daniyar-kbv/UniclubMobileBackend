# Generated by Django 3.1.3 on 2020-12-11 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_tg_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contacts',
            field=models.TextField(blank=True, null=True, verbose_name='Контактная информация'),
        ),
    ]
