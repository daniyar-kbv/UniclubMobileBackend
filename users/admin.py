from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile

admin.site.unregister(User)


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = ['id', 'username', 'date_joined']
