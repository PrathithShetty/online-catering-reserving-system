from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CateringUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Catering Info', {'fields': ('role', 'phone', 'address')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = UserAdmin.list_filter + ('role',)
