from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser',
              'groups']
    list_display = ['username', 'first_name', 'last_name', 'date_joined']

    def get_fields(self, request, obj=None):
        if not request.user.is_superuser:
            for field in ['is_staff', 'is_active', 'is_superuser', 'groups', 'password']:
                if self.fields.__contains__(field):
                    self.fields.remove(field)
        return self.fields

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(id=request.user.id)
        return qs
