from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import PartnershipApplication, BookingApplication, CourseBooking, LessonTime
from utils import general

import constants


@admin.register(PartnershipApplication)
class PartnershipApplication(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_processed', 'created_at']
    readonly_fields = ['id', 'created_at']
    list_filter = ['is_processed', 'created_at']
    fields = ['id', 'name', 'company_name', 'email', 'mobile_phone', 'is_processed', 'created_at']


class CourseBookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseBookingForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            lesson_times = LessonTime.objects.filter(weekday__course=self.instance.course)
            choices_1 = map(
                lambda time: (
                    time.id,
                    f'{general.get_value_from_choices(constants.WEEKDAYS, time.weekday.day)}:'
                    f' {time.from_time.strftime(constants.TIME_FORMAT_SHORT)}-'
                    f'{time.to_time.strftime(constants.TIME_FORMAT_SHORT)}'),
                lesson_times)
            choices_2 = map(
                lambda time: (
                    time.id,
                    f'{general.get_value_from_choices(constants.WEEKDAYS, time.weekday.day)}:'
                    f' {time.from_time.strftime(constants.TIME_FORMAT_SHORT)}-'
                    f'{time.to_time.strftime(constants.TIME_FORMAT_SHORT)}'),
                lesson_times)
            lesson_times_confirmed_widget = self.fields['lesson_times_confirmed'].widget
            lesson_times_confirmed_widget.choices = choices_1
            if self.fields.get('lesson_times'):
                lesson_times_widget = self.fields['lesson_times'].widget
                lesson_times_widget.choices = choices_2


class CourseBookingInline(admin.StackedInline):
    model = CourseBooking
    raw_id_fields = ['course']
    filter_horizontal = ['lesson_times', 'lesson_times_confirmed']
    extra = 0
    form = CourseBookingForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(course__user=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['lesson_times', 'course']
        return self.readonly_fields


@admin.register(BookingApplication)
class BookingApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'is_processed', 'created_at']
    list_filter = ['is_processed', 'created_at']
    fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'created_at', 'is_processed']
    readonly_fields = ['id', 'created_at']
    inlines = [CourseBookingInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(course_booking__course__user=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if not request.user.is_superuser:
            for field in ['first_name', 'last_name', 'is_processed']:
                readonly_fields.append(field)
        return readonly_fields

    def get_fields(self, request, obj=None):
        fields = self.fields
        if not request.user.is_superuser:
            for field in ['phone_number', 'email']:
                fields.remove(field)
        return fields
