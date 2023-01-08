from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db.models import Q

from core.utils import TitleMixin
from .models import Article, Category
from .mixins import ArticleAuthorRequiredMixin, ArticleEditorMixin, ArticleTitleMixin
from .forms import SearchForm
from .services import get_popular_categories


class ArticleCreateView(LoginRequiredMixin, TitleMixin, ArticleEditorMixin, CreateView):
    submit_button_text = 'Publish'
    title = 'New article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return redirect(article.get_absolute_url())


class ArticleDetailView(ArticleTitleMixin, DetailView):
    template_name = 'articles/article-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_articles"] = Article.objects.exclude(pk=self.object.pk).filter(category__name=self.object.category.name)[:2]
        context["popular_categories"] = get_popular_categories(limit=10)
        return context

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category'
        ).only(
            'author__first_name', 'author__last_name', 'author__username', 'author__avatar',
            'category__name',
            'title', 'slug', 'created_at', 'body', 'modified_at'
        )
    

class ArticleUpdateView(ArticleAuthorRequiredMixin, ArticleTitleMixin, ArticleEditorMixin, UpdateView):
    submit_button_text = 'Update'

    def get_queryset(self):
        return super().get_queryset().only(
            'category__name', 'title', 'slug', 'body', 'thumbnail', 'description'
        )


def article_delete(request, article_pk, article_slug):
    get_object_or_404(Article, pk=article_pk, slug=article_slug).delete()
    return redirect('index')


class ArticleListView(TitleMixin, ListView):
    model = Article
    template_name = 'articles/articles.html'
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


class ArticleSearchView(ArticleListView):
    template_name = 'articles/articles-search.html'
    query = None
    
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')

        if query:
            self.query = query.strip()

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        articles = super().get_queryset()

        if self.request.method == 'GET':
            form = SearchForm(self.request.GET)

            if form.is_valid():
                if self.query:
                    lookups = {'title__icontains', 'slug__icontains', 'description__icontains'}
                    query_filter = Q()

                    for lookup in lookups:
                        query_filter |= Q(**{lookup: self.query})

                    return articles.filter(query_filter)

            return Article.objects.none()

        return articles

    def get_title(self):
        return 'Search results for' + (f' "{self.query}"' if self.query else '')


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


class CategoryDetailView(TitleMixin, DetailView):
    model = Category
    template_name = 'articles/category-detail.html'
    context_object_name = 'category'
    title = 'Category'



class CategoryListView(TitleMixin, ListView):
    model = Category
    template_name = 'articles/category-list.html'
    context_object_name = 'categories'
    title = 'Categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_categories"] = get_popular_categories(limit=3)
        return context
