from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User

from rest_framework import serializers
from faker import Faker
from PIL import Image

from main.models import Course, CourseImage, LessonTime, WeekDay, AgeGroup, AdministrativeDivision, AttendanceType, \
    GradeType, GradeTypeGroup

import random, os, datetime, constants


class CourseImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        exclude = ['course']


class CourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        for i in range(3):
            image_nums = []
            while len(image_nums) != 3:
                rand = random.randint(1, 15)
                if not image_nums.__contains__(rand):
                    image_nums.append(rand)
            serializer = CourseImageCreateSerializer(data={
                'image': File(open(os.path.join(settings.BASE_DIR, f'media/test_photos/{image_nums[0]}.jpg'), 'rb')),
                'is_main': i == 0
            })
            serializer.is_valid(raise_exception=True)
            serializer.save(course=course)
        for weekday in WeekDay.objects.filter(course=course):
            lesson_count = random.randint(1, 6)
            lesson_times = []
            for i in range(lesson_count):
                lesson_time = random.randint(8, 17)
                while lesson_times.__contains__(lesson_time):
                    lesson_time = random.randint(8, 17)
                lesson_times.append(lesson_time)
                LessonTime.objects.create(
                    weekday=weekday,
                    from_time=datetime.datetime.strptime(f'{lesson_time if lesson_time >= 10 else "0{}".format(lesson_time)}:00:00', constants.TIME_FORMAT).time(),
                    to_time=datetime.datetime.strptime(f'{lesson_time + 1 if lesson_time + 1 >= 10 else "0{}".format(lesson_time + 1)}:00:00', constants.TIME_FORMAT).time()
                )
        return course


def create_courses(count=1):
    fake_lorem = Faker('la')

    for i in range(count):

        group = random.choice(list(map(lambda item: item.id, GradeTypeGroup.objects.all())))
        type_ = random.choice(list(map(lambda item: item.id, GradeType.objects.filter(group_id=group))))

        data = {
            "name": fake_lorem.sentence(nb_words=random.randint(1, 3)),
            "description": fake_lorem.paragraph(),
            "from_age": random.randint(1, 10),
            "to_age": random.randint(11, 18),
            "attendance_type": random.choice(list(map(lambda item: item.id, AttendanceType.objects.all()))),
            "grade_group": group,
            "grade_type": type_,
            "administrative_division": random.choice(list(map(lambda item: item.id, AdministrativeDivision.objects.all()))),
            "user": random.choice(list(map(lambda item: item.id, User.objects.filter(is_superuser=False))))
        }

        serializer = CourseCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
