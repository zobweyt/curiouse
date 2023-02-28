from functools import wraps

from django.http import Http404


def require_htmx(view_func):
    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        if not request.htmx:
            raise Http404
        return view_func(request, *args, **kwargs)

    return decorator
