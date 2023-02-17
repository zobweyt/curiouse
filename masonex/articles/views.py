from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from core.utils import TitleMixin
from .models import Article
from .mixins import ArticleEditorMixin, ArticleTitleMixin, ArticleAuthorRequiredMixin


class ArticleCreateView(LoginRequiredMixin, TitleMixin, ArticleEditorMixin, CreateView):
    title = 'New article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super().form_valid(form)
    

class ArticleUpdateView(ArticleAuthorRequiredMixin, ArticleTitleMixin, ArticleEditorMixin, UpdateView):
    def get_queryset(self):
        return super().get_queryset().only(
            'categories__id', 'title', 'slug', 'body', 'thumbnail'
        )


class ArticleDetailView(ArticleTitleMixin, DetailView):
    template_name = 'articles/article-detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["popular_categories"] = get_popular_categories(limit=10)
    #     related_articles = Article.objects.filter(categories__id=self.object.categories.id).exclude(pk=self.object.pk)[:3]
    #     context["related_articles"] = related_articles
    #     return context

    def get_queryset(self):
        return super().get_queryset().select_related('author').only(
            'author__first_name', 'author__last_name', 'author__username', 'author__avatar',
            'categories__name',
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
            'author__first_name', 'author__last_name', 
            'categories__name', 
            'title', 'thumbnail', 'slug'
        )
