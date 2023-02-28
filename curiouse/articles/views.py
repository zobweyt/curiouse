from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.templatetags.static import static

from core.utils import TitleMixin
from .models import Article, Author, Category
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
    paginate_by = 24
    title = 'Articles'
    
    def get_template_names(self):            
        if self.request.htmx:
            return 'articles/includes/article-list.html'
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
            return 'articles/includes/article-list.html'
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
    
    
def follow_author_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    author = Author.objects.get(user=user)
    author.followers.add(request.user)
    
    if request.htmx:
        return render(request, 'articles/includes/author-card.html', {'author': author})
    
    return redirect('articles:author_detail', username=username)


def unfollow_author_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    author = Author.objects.get(user=user)
    author.followers.remove(request.user)
    
    if request.htmx:
        return render(request, 'articles/includes/author-card.html', {'author': author})
    
    return redirect('articles:author_detail', username=username)


def save_article_view(request, pk, slug):
    article = get_object_or_404(Article, pk=pk, slug=slug)
    author = Author.objects.get(user=request.user)
    author.bookmarks.add(article)

    if request.htmx:
        return render(request, 'articles/includes/bookmark-button.html', {'viewer': author, 'article': article})
    
    return redirect('articles:article_detail', pk=pk, slug=slug)


def unsave_article_view(request, pk, slug):
    article = get_object_or_404(Article, pk=pk, slug=slug)
    author = Author.objects.get(user=request.user)
    author.bookmarks.remove(article)
    
    if request.htmx:
        return render(request, 'articles/includes/bookmark-button.html', {'viewer': author, 'article': article})
    
    return redirect('articles:article_detail', pk=pk, slug=slug)


class AuthorBookmarksView(ArticleListView):
    def get_queryset(self):
        author = Author.objects.get(user=self.request.user)
        return author.bookmarks.all()
    