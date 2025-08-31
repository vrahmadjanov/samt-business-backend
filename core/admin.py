from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import BusinessUser


@admin.register(BusinessUser)
class BusinessUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
