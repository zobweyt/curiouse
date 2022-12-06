from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from feed.forms import SearchForm
from feed.models import Post, User


class PostListingView(ListView):
    model = Post
    template_name = 'feed/index.html'
    context_object_name = 'posts'
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Masonex'
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'author')


class CategoryView(PostListingView):
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs['category_slug'])


class PostSearchView(ListView):
    model = Post
    template_name = 'feed/search.html'
    extra_context = {'form': SearchForm}
    context_object_name = 'results'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context['title'] = 'Search ' + (query if query else '')
        return context

    def get_queryset(self):
        posts = super().get_queryset().select_related('category', 'author')

        if self.request.method == 'GET':
            form = SearchForm(self.request.GET)

            if form.is_valid():
                query = form.data.get('query')

                if query:
                    query = query.strip()
                    lookups = Q(title__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query)
                    return posts.filter(lookups)

            return Post.objects.none()

        return posts


class AuthorDetailView(PostListingView, ListView):
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
