from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CareerApplication, ContactMessage


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('MamaCare Fields', {'fields': ('role', 'is_approved', 'license_number', 'assigned_staff')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('MamaCare Fields', {'fields': ('role', 'is_approved', 'license_number')}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(CareerApplication)
admin.site.register(ContactMessage)