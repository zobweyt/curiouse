from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from core.utils import TitleMixin
from .models import Article, Category
from .decorators import require_article_author
from .mixins import ArticleEditorMixin, ArticleTitleMixin
from .services import get_popular_categories


class ArticleCreateView(LoginRequiredMixin, TitleMixin, ArticleEditorMixin, CreateView):
    title = 'New article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super().form_valid(form)
    

class ArticleUpdateView(ArticleTitleMixin, ArticleEditorMixin, UpdateView):
    def get_queryset(self):
        return super().get_queryset().only(
            'category__id', 'title', 'slug', 'body', 'thumbnail', 'description'
        )


class ArticleDetailView(ArticleTitleMixin, DetailView):
    template_name = 'articles/article-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_categories"] = get_popular_categories(limit=10)
        return context

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category'
        ).only(
            'author__first_name', 'author__last_name', 'author__username', 'author__avatar',
            'category__name',
            'title', 'slug', 'created_at', 'body'
        )


@require_article_author
def article_delete_view(request, pk, slug):
    get_object_or_404(Article, pk=pk, slug=slug).delete()
    messages.success(request, 'The article has been successfully deleted.')
    return redirect('articles:article_list')


class ArticleListView(TitleMixin, ListView):
    model = Article
    template_name = 'articles/article-list.html'
    context_object_name = 'articles'
    paginate_by = 24
    title = 'Articles'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category'
        ).only(
            'author__first_name', 'author__last_name', 
            'category__name', 
            'title', 'thumbnail', 'slug'
        )


class AuthorArticleListView(ArticleListView):
    template_name = 'articles/article-author.html'

    def get(self, request, *args, **kwargs):
        self.author = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

    def get_queryset(self):
        return super().get_queryset().filter(author=self.author)

    def get_title(self):
        return self.author.get_full_name()


class CategoryDetailView(ArticleListView):
    def get(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().filter(category__id=self.category.id)
    
    def get_title(self):
        return self.category
