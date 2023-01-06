from django.db.models import Count

from .models import Category


def get_popular_categories(limit: int = 21):
    return Category.objects.annotate(articles_count=Count("article")).order_by("-articles_count")[:limit]
