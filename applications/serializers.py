from rest_framework import serializers

from main.models import LessonTime
from .models import BookingApplication, PartnershipApplication, CourseBooking


class BookingApplicationCreateSerializer(serializers.ModelSerializer):
    lesson_times = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = BookingApplication
        fields = '__all__'

    def create(self, validated_data):
        lesson_times = validated_data.pop('lesson_times')
        application = BookingApplication.objects.create(**validated_data)
        courses = []
        times = LessonTime.objects.filter(id__in=lesson_times)
        for lesson_time in lesson_times:
            try:
                time = LessonTime.objects.get(id=lesson_time)
            except:
                application.delete()
                raise serializers.ValidationError({
                    'lesson_times': 'Время занятия не найдено'
                })
            if time.weekday.course not in courses:
                courses.append(time.weekday.course)
        for course in courses:
            booking = CourseBooking.objects.create(
                booking_application=application,
                course=course
            )
            booking.lesson_times.set(times.filter(weekday__course=course))
        application._created = True
        application.save()
        return application


class PartnershipApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipApplication
        fields = '__all__'
