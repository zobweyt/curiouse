from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import UpdateView

from .models import Post


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if not request.user.is_staff and request.user.pk != object.author.pk:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class ExcludeAuthenticatedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm lh-sm'})


class PostsMixin:
    model = Post
    template_name = 'feed/index.html'
    context_object_name = 'posts'
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Masonex'
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'author')


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
