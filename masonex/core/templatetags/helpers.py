from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_class(context, url_to_check, exact=True):
    path = context['request'].path
    url = reverse(url_to_check)
    if path.__contains__(url) if exact else path == url:
        return ' active'
    return ''


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Usege: `{{ "aaa"|replace:"a|b" }}`
    """
    what, to = arg.split('|')
    return value.replace(what, to)
