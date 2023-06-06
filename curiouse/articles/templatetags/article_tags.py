from django import template

from articles.models import Author

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.simple_tag(takes_context=True)
def get_author(context, user=None):
    user = user or context['request'].user
    author = Author.objects.get(user=user)
    return author


@register.simple_tag(takes_context=True)
def get_bookmark_count(context):
    author = get_author(context)
    bookmark_count = author.bookmarks.count()
    return bookmark_count
