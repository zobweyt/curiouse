from django import template
from django.urls import reverse
from django.utils.timesince import timesince

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
    Usage: `{{ "aaa"|replace:"a|b" }}`
    Output: `bbb`
    """
    what, to = arg.split('|')
    return value.replace(what, to)


@register.filter
def relative(value, now=None, depth=1):
    time = timesince(value, now, depth=depth)
    return f'{time} ago'


@register.filter(name='range')
def filter_range(times):
    return range(times)
