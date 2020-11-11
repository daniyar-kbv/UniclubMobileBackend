from django.contrib import admin

from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import Course, WeekDay, LessonTime, CourseImage


class LessonTimeInline(NestedTabularInline):
    model = LessonTime
    extra = 0


class WeekdayInline(NestedTabularInline):
    model = WeekDay
    extra = 0
    inlines = [LessonTimeInline]
    readonly_fields = ['day']


class CourseImageInline(NestedTabularInline):
    model = CourseImage
    extra = 0


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    inlines = [CourseImageInline, WeekdayInline]
