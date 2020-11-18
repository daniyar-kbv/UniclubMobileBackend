# Generated by Django 3.1.3 on 2020-11-17 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_course_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='courseimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='courseimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='lessontime',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='lessontime',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='weekday',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='weekday',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
    ]
