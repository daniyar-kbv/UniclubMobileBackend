from django.contrib import admin

from .models import AgeGroup, AttendanceType, AdministrativeDivision, GradeTypeGroup, GradeType


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(AdministrativeDivision)
class AdministrativeDivisionAdmin(admin.ModelAdmin):
    pass


class GradeTypeInline(admin.TabularInline):
    model = GradeType
    extra = 0


@admin.register(GradeTypeGroup)
class GradeTypeGroupAdmin(admin.ModelAdmin):
    inlines = [GradeTypeInline]
