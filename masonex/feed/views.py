from hitcount.views import HitCountDetailView

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from feed.forms import PostForm, UserLoginForm, UserRegistrationForm, ProfileForm, SearchForm
from feed.models import Post, User
from feed.utils import ExcludeAuthenticatedUsersMixin, AuthorRequiredMixin, PostsMixin, PostMixin


class HomeView(PostsMixin, ListView):
    pass


class CategoryView(PostsMixin, ListView):
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs['category_slug'])


class SearchView(ListView):
    model = Post
    template_name = 'feed/search.html'
    extra_context = {'title': 'Search', 'form': SearchForm}
    context_object_name = 'results'
    paginate_by = 12

    def get_queryset(self):
        posts = super().get_queryset().select_related('category', 'author')

        if self.request.method == 'GET':
            form = SearchForm(self.request.GET)
            query = form.data.get('query')

            if query:
                query = query.strip()
                lookups = Q(title__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query)
                return posts.filter(lookups)

        return posts


class PostDetailView(PostMixin, HitCountDetailView):
    template_name = 'feed/post_detail.html'
    count_hit = True


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'feed/post_create.html'
    extra_context = {'title': 'Create post'}

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(post.get_absolute_url())


class PostUpdateView(AuthorRequiredMixin, PostMixin, UpdateView):
    form_class = PostForm
    template_name = 'feed/post_update.html'


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'feed/profile.html'
    extra_context = {'title': 'Profile'}

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


class UserAuthenticiationView(ExcludeAuthenticatedUsersMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'feed/login.html'
    extra_context = {'title': 'Sign in'}

    def get_success_url(self):
        return reverse_lazy('home')


class UserRegistrationView(ExcludeAuthenticatedUsersMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'feed/register.html'
    extra_context = {'title': 'Sign up'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')
