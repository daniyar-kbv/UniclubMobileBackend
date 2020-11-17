from django.contrib import admin

from .models import PartnershipApplication, BookingApplication

@admin.register(PartnershipApplication)
class PartnershipApplication(admin.ModelAdmin):
    pass


@admin.register(BookingApplication)
class BookingApplication(admin.ModelAdmin):
    pass
