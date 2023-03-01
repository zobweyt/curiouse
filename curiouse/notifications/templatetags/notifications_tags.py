from django import template

from notifications.models import Notification

register = template.Library()


@register.simple_tag(takes_context=True)
def has_new_notifications(context):
    has_new = Notification.objects.filter(recipient=context['user']).exists()
    return has_new
