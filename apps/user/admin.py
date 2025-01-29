from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name')
