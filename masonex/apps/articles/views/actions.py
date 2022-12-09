from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView


from core.utils import TitleMixin
from .utils import ArticleAuthorRequiredMixin, ArticleEditorMixin, ArticleMixin
from articles.models import Article


class ArticleCreateView(LoginRequiredMixin, ArticleEditorMixin, TitleMixin, CreateView):
    form_action = reverse_lazy('article_create')
    form_submit_button_text = 'Publish'
    title = 'Create article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return redirect(article.get_absolute_url())


class ArticleDetailView(ArticleMixin, DetailView):
    template_name = 'articles/article_detail.html'
    

class ArticleUpdateView(ArticleAuthorRequiredMixin, ArticleMixin, ArticleEditorMixin, UpdateView):
    form_submit_button_text = 'Update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['action'] = reverse_lazy('article_update', kwargs={
            self.pk_url_kwarg: article.pk, self.slug_url_kwarg: article.slug
        })
        return context


def article_delete(request, article_pk, article_slug):
    get_object_or_404(Article, pk=article_pk, slug=article_slug).delete()
    return redirect('home')
