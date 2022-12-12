from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def truncatemail(email: str, chars: int) -> str:
    domain = email.split('@')[-1]
    return f'{email[0:chars]}***@{domain}'
