from django.contrib import admin
from django.utils.html import format_html

from .models import PartnershipApplication, BookingApplication, CourseBooking


@admin.register(PartnershipApplication)
class PartnershipApplication(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


class CourseBookingInline(admin.StackedInline):
    model = CourseBooking
    raw_id_fields = ['course']
    extra = 0

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
    inlines = [CourseBookingInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(course_booking__course__user=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['first_name', 'last_name', 'phone_number', 'email']
        return self.readonly_fields
