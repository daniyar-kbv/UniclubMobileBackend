# Generated by Django 3.1.3 on 2020-11-28 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20201117_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-created_at'], 'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
    ]
