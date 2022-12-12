from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def truncatemail(email: str, chars: int) -> str:
    name, domain = email.split('@')
    return f'{name[0:chars]}***@{domain}'
