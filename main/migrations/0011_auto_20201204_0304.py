# Generated by Django 3.1.3 on 2020-12-03 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_coursereview_telegramuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
