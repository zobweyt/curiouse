import re

from django import template
from django.http import QueryDict
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_list(dictionary: QueryDict, key: str) -> list:
    return dictionary.getlist(key)


@register.filter()
@stringfilter
def highlight(text: str, to_highlight: str) -> str:
    pattern = f'{to_highlight.strip()}+'
    repl = r'<mark>\g<0></mark>'
    highlighted_text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return mark_safe(highlighted_text)


@register.filter
@stringfilter
def truncatemail(email: str, chars: int) -> str:
    domain = email.split('@')[-1]
    return f'{email[0:chars]}***@{domain}'


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()

