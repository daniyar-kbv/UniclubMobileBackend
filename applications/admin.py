from django.contrib import admin

from .models import PartnershipApplication, BookingApplication, CourseBooking


@admin.register(PartnershipApplication)
class PartnershipApplication(admin.ModelAdmin):
    pass


class CourseBookingInline(admin.StackedInline):
    model = CourseBooking


@admin.register(BookingApplication)
class BookingApplicationAdmin(admin.ModelAdmin):
    inlines = [CourseBookingInline]
