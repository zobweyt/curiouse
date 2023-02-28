from django.views.generic import UpdateView
from django.core.exceptions import PermissionDenied

from core.utils import TitleMixin
from articles.models import Article
from articles.forms import ArticleEditorForm


class ArticleAuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user.pk != self.get_object().author.pk:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        if not hasattr(self, '_object'):
            self._object = super().get_object()
        return self._object


class ArticleEditorMixin:
    form_class = ArticleEditorForm
    template_name = 'articles/article-editor.html'


class ArticleTitleMixin(TitleMixin):
    model = Article
    context_object_name = 'article'

    def get_title(self):
        is_update_view = issubclass(self.__class__, UpdateView)
        return ('Edit: ' if is_update_view else '') + self.object.title
