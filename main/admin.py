from django.contrib import admin
from django import forms
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import Course, WeekDay, LessonTime, CourseImage, CourseReview
from other.models import GradeType, GradeTypeGroup
import operator


class CourseListFilter(admin.SimpleListFilter):
    title = 'Занятия'
    parameter_name = 'course'

    def lookups(self, request, model_admin):
        return map(lambda course: (course.id, course.name), Course.objects.filter(user=request.user))

    def queryset(self, request, queryset):
        return queryset.filter(course_id=self.value()) if self.value() else queryset


class CourseListGradeTypeFilter(admin.SimpleListFilter):
    title = 'Вид занятия'
    parameter_name = 'grade_type'

    def lookups(self, request, model_admin):
        return map(
            lambda type:
            (type.id, type.name),
            filter(
                lambda type:
                type.courses.filter(user=request.user).count() > 0,
                list(GradeType.objects.all())
            )
        )

    def queryset(self, request, queryset):
        return queryset.filter(grade_type_id=self.value()) if self.value() else queryset


class CourseReviewInline(NestedTabularInline):
    model = CourseReview
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            self.readonly_fields = ['user', 'text', 'is_anonymous']
        return self.readonly_fields


class LessonTimeInline(NestedTabularInline):
    model = LessonTime
    extra = 0


class WeekdayInline(NestedTabularInline):
    model = WeekDay
    extra = 0
    inlines = [LessonTimeInline]
    readonly_fields = ['day']
    template = 'tabular_nested_custom.html'

    def has_add_permission(self, request, obj):
        return False


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
    list_display = ['name', 'created_at']
    list_filter = []
    inlines = [CourseImageInline, WeekdayInline, CourseReviewInline]

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

    def get_list_filter(self, request):
        if not request.user.is_superuser and not self.list_filter.__contains__(CourseListGradeTypeFilter):
            self.list_filter.append(CourseListGradeTypeFilter)
        elif request.user.is_superuser and not self.list_filter.__contains__('grade_type'):
            self.list_filter.append('grade_type')
        return self.list_filter


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'text', 'created_at', 'is_anonymous']
    list_filter = ['created_at', 'is_anonymous']
    fields = ['user', 'course', 'text', 'is_anonymous']
    readonly_fields = ['user', 'course', 'text', 'is_anonymous']

    def get_list_filter(self, request):
        if not request.user.is_superuser and not self.list_filter.__contains__(CourseListFilter):
            self.list_filter.append(CourseListFilter)
        elif request.user.is_superuser and not self.list_filter.__contains__('course'):
            self.list_filter.append('course')
        return self.list_filter

    def get_fields(self, request, obj=None):
        if obj.is_anonymous:
            self.fields.remove('user')
        return self.fields
