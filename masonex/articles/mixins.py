from django.views.generic import UpdateView

from core.utils import TitleMixin
from articles.models import Article
from articles.forms import ArticleEditorForm


class ArticleEditorMixin:
    form_class = ArticleEditorForm
    template_name = 'articles/article-editor.html'


class ArticleTitleMixin(TitleMixin):
    model = Article
    context_object_name = 'article'

    def get_title(self):
        is_update_view = self.__class__.__bases__.__contains__(UpdateView)
        return ('Edit: ' if is_update_view else '') + self.object.title
