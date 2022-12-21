from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from core.utils import TitleMixin
from articles.models import Article
from articles.forms import ArticleEditorForm


class ArticleAuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user.pk != self.get_object().author.pk:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        if not hasattr(self, '_object'):
            self._object = super().get_object()
        return self._object


class ArticleEditorMixin:
    form_class = ArticleEditorForm
    template_name = 'articles/article_editor.html'
    submit_button_text = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_text'] = self.submit_button_text            
        return context


class ArticleTitleMixin(TitleMixin):
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'article_pk'
    slug_url_kwarg = 'article_slug'

    def get_title(self):
        is_update_view = self.__class__.__bases__.__contains__(UpdateView)
        return ('Edit: ' if is_update_view else '') + self.object.title
