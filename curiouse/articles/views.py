from core.decorators import require_htmx
from core.utils import TitleMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .mixins import (
    ArticleAuthorRequiredMixin,
    ArticleEditorMixin,
    ArticleTitleMixin
)
from .models import Article, Author, Category


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewer'] = Author.objects.get(user=self.request.user)
        
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('author').only(
            'author__user__first_name', 'author__user__last_name', 'author__user__avatar', 'author__user__bio',
            'title', 'slug', 'created_at', 'body'
        )


class ArticleListView(TitleMixin, ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 4
    title = 'Articles'
    
    def get_template_names(self):            
        if self.request.htmx:
            return 'articles/includes/article-listing.html'
        return 'articles/article-list.html'

    def get_queryset(self):
        return super().get_queryset().select_related('author', 'author__user').prefetch_related('categories')
        
        
class AuthorDetailView(ArticleListView):
    def get(self, *args, **kwargs):
        user = get_object_or_404(get_user_model(), username=kwargs.get('username'))
        self.author = Author.objects.get(user=user)
        return super().get(*args, **kwargs)
    
    def get_template_names(self):
        if self.request.htmx:
            return 'articles/includes/article-listing.html'
        return 'articles/author-detail.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.author)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context
    
    def get_title(self):
        return self.author


class AuthorBookmarksView(ArticleListView):
    def get_queryset(self):
        author = Author.objects.get(user=self.request.user)
        return author.bookmarks.all()


class AuthorSubscriptionsView(ArticleListView):
    def get_queryset(self):
        author = Author.objects.get(user=self.request.user)
        return super().get_queryset().filter(author__followers=author.user)
    

@require_htmx
def follow_author_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    author = Author.objects.get(user=user)
    author.followers.add(request.user)
    
    return render(request, 'articles/includes/author-card.html', {'author': author})    


@require_htmx
def unfollow_author_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    author = Author.objects.get(user=user)
    author.followers.remove(request.user)
    
    return render(request, 'articles/includes/author-card.html', {'author': author})


@require_htmx
def save_article_view(request, pk, slug):
    article = get_object_or_404(Article, pk=pk, slug=slug)
    author = Author.objects.get(user=request.user)
    author.bookmarks.add(article)

    return render(request, 'articles/includes/bookmark-button.html', {'viewer': author, 'article': article})


@require_htmx
def unsave_article_view(request, pk, slug):
    article = get_object_or_404(Article, pk=pk, slug=slug)
    author = Author.objects.get(user=request.user)
    author.bookmarks.remove(article)
    
    return render(request, 'articles/includes/bookmark-button.html', {'viewer': author, 'article': article})    
