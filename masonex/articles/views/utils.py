from django.http import Http404
from django.views.generic import UpdateView

from articles.models import Article
from articles.forms import ArticleEditorForm


class ArticleAuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        
        if not request.user.is_staff and request.user.pk != object.author.pk:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)


class ArticleEditorMixin:
    form_class = ArticleEditorForm
    template_name = 'feed/article_editor.html'
    form_action = None
    form_submit_button_text = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit'] = self.form_submit_button_text
        
        if self.form_action:
            context['action'] = self.form_action
            
        return context


class ArticleMixin:
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'article_pk'
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_update_view = self.__class__.__bases__.__contains__(UpdateView)
        context['title'] = ('Edit: ' if is_update_view else '') + self.object.title
        return context
