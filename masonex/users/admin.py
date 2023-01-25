from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined', 'is_staff')
    list_display_links = ('username',)
    list_filter = ('date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'bio')
