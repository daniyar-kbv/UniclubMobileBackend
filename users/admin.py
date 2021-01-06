from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms

from .models import Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileInline]
    fieldsets = [
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    ]
    list_display = ['username', 'first_name', 'last_name', 'date_joined']

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return self.fieldsets[:2]
        return self.fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(id=request.user.id)
        return qs

    def get_list_filter(self, request):
        if not request.user.is_superuser:
            return []
        return self.list_filter

    def get_search_fields(self, request):
        if not request.user.is_superuser:
            return []
        return self.search_fields