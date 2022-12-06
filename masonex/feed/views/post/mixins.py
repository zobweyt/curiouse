from django.http import Http404
from django.views.generic import UpdateView

from feed.models import Post


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if not request.user.is_staff and request.user.pk != object.author.pk:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class PostMixin:
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_update_view = self.__class__.__bases__.__contains__(UpdateView)
        context['title'] = ('Edit: ' if is_update_view else '') + self.object.title
        return context
