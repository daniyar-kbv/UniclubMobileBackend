from rest_framework import serializers

from .models import Course, LessonTime, WeekDay
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
    attendance_type = AttendanceTypeSerializer()
    administrative_division = AdministrativeDivisionSerializer()
    grade_group = GradeTypeGroupSerializer()
    grade_type = GradeTypeListSerializer()

    class Meta:
        model = Course
        fields = '__all__'
