from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from core.utils import TitleMixin
from accounts.models import User
from articles.forms import SearchForm
from articles.models import Category, Article


class ArticleListView(TitleMixin, ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    paginate_by = 16
    title = 'Articles'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category'
        ).only(
            'author__first_name', 'author__last_name', 'category__name', 'title', 'thumbnail', 'slug'
        )


class ArticleCategoryListView(ArticleListView):
    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs['category_slug']
        )

    def get_title(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])


class ArticleSearchView(ArticleListView, ListView):
    template_name = 'articles/article_search.html'
    extra_context = {'form': SearchForm}
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


class AuthorArticleListView(ArticleListView, ListView):
    template_name = 'articles/author_detail.html'

    def get(self, request, *args, **kwargs):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

    def get_queryset(self):
        return super().get_queryset().filter(author=self.author)

    def get_title(self):
        return self.author.get_full_name()
