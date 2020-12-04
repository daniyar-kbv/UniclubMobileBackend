from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile

admin.site.unregister(User)


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser',
              'groups']
    list_display = ['username', 'first_name', 'last_name', 'date_joined']

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(id=request.user.id)
        return qs
