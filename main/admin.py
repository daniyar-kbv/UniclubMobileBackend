from django.contrib import admin

from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import Course, WeekDay, LessonTime


class LessonTimeInline(NestedTabularInline):
    model = LessonTime
    extra = 0


class WeekdayInline(NestedTabularInline):
    model = WeekDay
    extra = 0
    inlines = [LessonTimeInline]
    readonly_fields = ['day']


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    inlines = [WeekdayInline]
