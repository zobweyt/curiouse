from django.template.defaultfilters import stringfilter, register
from django.utils.safestring import mark_safe
import re


@register.filter
def get_list(dictionary: dict, key: str) -> list:
    return dictionary.getlist(key)


@register.filter
@stringfilter
def highlight(text: str, to_highlight: str) -> str:
    return mark_safe(re.sub(f'({to_highlight})', r'<mark class="p-0">\1</mark>', text, flags=re.IGNORECASE))
