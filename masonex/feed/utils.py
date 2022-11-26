from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.forms.fields import CharField, ChoiceField

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


class CharFieldCSSClassMixin:
    """Adds custom CSS class to every CharField in a form."""

    input_css_class = 'form-control'
    input_font_size_css_class = 'sm'

    def __init__(self, *args, **kwargs):
        if not self.input_css_class:
            raise AttributeError('input_css_class must be provided.')

        classes = [self.input_css_class]

        if self.input_font_size_css_class:
            classes.append(f'{self.input_css_class}-{self.input_font_size_css_class}')

        formated_classes = ' '.join(classes)

        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if isinstance(field, CharField) or isinstance(field, ChoiceField):
                field.widget.attrs.update({'class': formated_classes})


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
