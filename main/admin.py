from django.contrib import admin
from django import forms
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import Course, WeekDay, LessonTime, CourseImage
from other.models import GradeType, GradeTypeGroup
import operator


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


def tagform_factory(group):
    class TypeForm(forms.ModelForm):
        grade_type = forms.ModelChoiceField(
            queryset=GradeType.objects.filter(group=group)
        )
    return TypeForm


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    list_display = ['id', 'name', 'created_at']
    inlines = [CourseImageInline, WeekdayInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

    def get_fields(self, request, obj=None):
        if self.fields:
            return self.fields
        form = self._get_form_for_get_fields(request, obj)
        if not request.user.is_superuser:
            del form.base_fields['user']
        return [*form.base_fields, *self.get_readonly_fields(request, obj)]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None and obj.grade_group is not None:
            kwargs['form'] = tagform_factory(obj.grade_group)
        return super(CourseAdmin, self).get_form(request, obj, **kwargs)
