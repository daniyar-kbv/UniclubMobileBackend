# Generated by Django 3.1.3 on 2020-11-17 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20201112_0020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseimage',
            options={'ordering': ['is_main', 'id'], 'verbose_name': 'Фото курса', 'verbose_name_plural': 'Фото курсов'},
        ),
    ]
