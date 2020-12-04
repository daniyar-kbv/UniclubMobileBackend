from django.db.models import Count

from rest_framework import serializers

from .models import Course, LessonTime, WeekDay, CourseImage
from other.serializers import AgeGroupSerializer, AttendanceTypeSerializer, AdministrativeDivisionSerializer, \
    GradeTypeGroupSerializer, GradeTypeListSerializer
from users.models import User, Profile

import random


class CourseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['tg_username', 'website_url']


class CourseUserSerializer(serializers.ModelSerializer):
    profile = CourseProfileSerializer()

    class Meta:
        model = User
        fields = ['profile']


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
    user = CourseUserSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'images', 'weekdays', 'user']

    def get_weekdays(self, obj):
        weekdays = obj.weekdays.annotate(num_times=Count('lesson_times')).filter(num_times__gt=0).order_by('day')
        serializer = WeekdayListSerializer(weekdays, many=True)
        return serializer.data

    def get_images(self, obj):
        images = CourseImage.objects.filter(course=obj)
        urls = []
        for image in images:
            url = f'{image.image.url}'.replace('/media/uniclub_mobile/media/test_photos/', '/media/test_photos/')
            urls.append(self.context.get('request').build_absolute_uri(url))
        return urls

