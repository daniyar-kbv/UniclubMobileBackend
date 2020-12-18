from django.contrib import admin

from .models import AgeGroup, AttendanceType, AdministrativeDivision, GradeTypeGroup, GradeType


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(AdministrativeDivision)
class AdministrativeDivisionAdmin(admin.ModelAdmin):
    search_fields = ['name']


class GradeTypeInline(admin.TabularInline):
    model = GradeType
    extra = 0


@admin.register(GradeTypeGroup)
class GradeTypeGroupAdmin(admin.ModelAdmin):
    inlines = [GradeTypeInline]
    search_fields = ['name']


@admin.register(GradeType)
class GradeTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}