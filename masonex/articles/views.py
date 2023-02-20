from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from core.utils import TitleMixin
from .models import Article, Author
from .mixins import ArticleEditorMixin, ArticleTitleMixin, ArticleAuthorRequiredMixin


class ArticleCreateView(LoginRequiredMixin, TitleMixin, ArticleEditorMixin, CreateView):
    title = 'New article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)
    

class ArticleUpdateView(ArticleAuthorRequiredMixin, ArticleTitleMixin, ArticleEditorMixin, UpdateView):
    def get_queryset(self):
        return super().get_queryset().only(
            'categories__id', 'title', 'slug', 'body', 'thumbnail'
        )


class ArticleDetailView(ArticleTitleMixin, DetailView):
    template_name = 'articles/article-detail.html'

    def get_queryset(self):
        return super().get_queryset().select_related('author').only(
            'author__user__first_name', 'author__user__last_name', 'author__user__avatar', 'author__user__bio',
            'title', 'slug', 'created_at', 'body'
        )


class ArticleListView(TitleMixin, ListView):
    model = Article
    template_name = 'articles/article-list.html'
    context_object_name = 'articles'
    paginate_by = 24
    title = 'Articles'

    def get_queryset(self):
        return super().get_queryset().select_related('author').only(
            'author__user__first_name', 'author__user__last_name', 
            'categories__name', 
            'title', 'thumbnail', 'slug'
        )
