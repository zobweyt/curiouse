from django.shortcuts import redirect

from feed.models import Post, User


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    

class PostAuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs[self.pk_url_kwarg])
        if not request.user.is_staff and request.user.pk != post.author.pk:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ExcludeAuthenticatedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class InputClassMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-sm lh-sm'}
            )
