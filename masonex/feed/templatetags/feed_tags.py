from django.template.defaultfilters import stringfilter, register
from django.utils.safestring import mark_safe
from re import sub, IGNORECASE


@register.filter
def get_list(dictionary: dict, key: str) -> list:
    return dictionary.getlist(key)


@register.filter
@stringfilter
def highlight(text: str, to_highlight: str) -> str:
    return mark_safe(sub(f'({to_highlight})', r'<mark class="p-0">\1</mark>', text, flags=IGNORECASE))
