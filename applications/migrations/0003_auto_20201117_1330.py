# Generated by Django 3.1.3 on 2020-11-17 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20201111_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursebooking',
            name='booking_application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_booking', to='applications.bookingapplication', verbose_name='Заявка на бронирование'),
        ),
    ]
