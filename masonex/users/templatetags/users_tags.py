from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_class(context, url_to_check):
    if context['request'].path.__contains__(reverse(url_to_check)):
        return ' active'
    return ''
