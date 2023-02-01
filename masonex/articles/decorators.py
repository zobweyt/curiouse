from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Article


def require_article_author(view_func):
    wraps(view_func)
    def wrapper(request, pk, slug):
        article = get_object_or_404(Article, pk=pk, slug=slug)
        if request.user.is_staff or request.user.pk == article.author.pk:
            return view_func(request, pk=pk, slug=slug)
        else:
            raise PermissionDenied
        
    return wrapper
