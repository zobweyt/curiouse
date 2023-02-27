from django.contrib import admin

from core.templatetags.helpers import relative
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'ago')
    list_display_links = ('__str__',)
    search_fields = ('__str__',)
    list_filter = ('created_at',)
    
    def ago(self, obj):
        return relative(obj.created_at)
