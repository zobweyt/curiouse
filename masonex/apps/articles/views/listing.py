from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from articles.forms import SearchForm
from articles.models import Article
from accounts.models import User


class ArticleListView(ListView):
    model = Article
    template_name = 'feed/index.html'
    context_object_name = 'articles'
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Masonex'
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'author')


class ArticleCategoryListView(ArticleListView):
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs['category_slug'])


class ArticleSearchView(ArticleListView, ListView):
    template_name = 'feed/article_search.html'
    extra_context = {'form': SearchForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context['title'] = 'Search ' + (query if query else '')
        return context

    def get_queryset(self):
        posts = super().get_queryset()

        if self.request.method == 'GET':
            form = SearchForm(self.request.GET)

            if form.is_valid():
                query = form.data.get('query')

                if query:
                    query = query.strip()
                    lookups = {'title__icontains', 'slug__icontains', 'description__icontains'}
                    query_filter = Q()

                    for lookup in lookups:
                        query_filter |= Q(**{lookup: query})
                        print(query_filter)

                    return posts.filter(query_filter)

            return Article.objects.none()

        return posts


class AuthorArticleListView(ArticleListView, ListView):
    template_name = 'feed/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'title': self.author.get_full_name(),
            'author': self.author,
        }
        return context | extra_context

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return super().get_queryset().filter(author=self.author)
