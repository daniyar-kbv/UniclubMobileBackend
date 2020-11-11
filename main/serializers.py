from rest_framework import serializers

from .models import Course, LessonTime, WeekDay, CourseImage
from other.serializers import AgeGroupSerializer, AttendanceTypeSerializer, AdministrativeDivisionSerializer, \
    GradeTypeGroupSerializer, GradeTypeListSerializer


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
    weekdays = WeekdayListSerializer(many=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'images', 'weekdays']

    def get_images(self, obj):
        images = CourseImage.objects.filter(course=obj)
        urls = []
        for image in images:
             urls.append(self.context.get('request').build_absolute_uri(image.image.url))
        return urls

