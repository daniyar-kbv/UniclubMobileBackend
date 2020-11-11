# Generated by Django 3.1.3 on 2020-11-11 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201111_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False, verbose_name='Основное')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Изображение курсоа',
                'verbose_name_plural': 'Изображения курсов',
            },
        ),
    ]
