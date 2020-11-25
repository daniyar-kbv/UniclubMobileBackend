from django.db.models import Count

from rest_framework import serializers

from .models import Course, LessonTime, WeekDay, CourseImage
from other.serializers import AgeGroupSerializer, AttendanceTypeSerializer, AdministrativeDivisionSerializer, \
    GradeTypeGroupSerializer, GradeTypeListSerializer

import random


class LessonTimeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTime
        exclude = ['weekday']


class WeekdayListSerializer(serializers.ModelSerializer):
    lesson_times = LessonTimeListSerializer(many=True)

    class Meta:
        model = WeekDay
        exclude = ['course']


class CourseListSerializer(serializers.ModelSerializer):
    weekdays = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'images', 'weekdays']

    def get_weekdays(self, obj):
        weekdays = obj.weekdays.annotate(num_times=Count('lesson_times')).filter(num_times__gt=0)
        serializer = WeekdayListSerializer(weekdays, many=True)
        return serializer.data

    def get_images(self, obj):
        images = CourseImage.objects.filter(course=obj)
        urls = []
        for image in images:
            url = f'{image.image.url}'.replace('/media/uniclub_mobile/media/test_photos/', '/media/test_photos/')
            urls.append(self.context.get('request').build_absolute_uri(url))
        return urls

