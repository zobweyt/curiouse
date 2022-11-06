import operator
from datetime import datetime, date, timedelta
from functools import reduce
from hitcount.views import HitCountDetailView

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from feed.forms import PostForm, UserLoginForm, UserRegistrationForm, ProfileForm, SearchForm
from feed.models import Post, Category, User
from feed.utils import ExcludeAuthenticatedUsersMixin, PostAuthorRequiredMixin

# add mixin to populate post title


class HomeView(ListView):
    model = Post
    template_name = 'feed/index.html'
    extra_context = {'title': 'Masonex', 'categories': Category.objects.all()[:4]}
    context_object_name = 'posts'
    paginate_by = 16

    def get_queryset(self):
        return super().get_queryset().select_related('category', 'author')


class CategoryView(ListView):
    model = Post
    template_name = 'feed/index.html'
    extra_context = {'title': 'Masonex', 'categories': Category.objects.all()[:4]}
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs['category_slug']).select_related('category', 'author')


class SearchView(ListView):
    model = Post
    template_name = 'feed/search.html'
    extra_context = {'title': 'Search', 'categories': Category.objects.all(), 'form': SearchForm}
    context_object_name = 'results'
    paginate_by = 12

    # refactor the method below
    def get_queryset(self):
        if self.request.method == 'GET':
            form = SearchForm(self.request.GET)
            lookups = Q()

            query = form.data.get('query')
            if query:
                query = query.strip()
                lookups &= Q(title__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query)

            categories = form.data.getlist('category')
            if categories:
                pairs = (Q(category_id=int(pk)) for pk in categories)
                lookups &= reduce(operator.or_, pairs)

            published = form.data.get('published')
            if published:
                if published == 'today':
                    lookups &= Q(create_date__day=datetime.utcnow().day)
                if published == 'week':
                    lookups &= Q(create_date__day__range=[datetime.utcnow().day - datetime.utcnow().weekday(), datetime.utcnow().day])
                if published == 'month':
                    lookups &= Q(create_date__month=datetime.now().month)
                if published == 'year':
                    lookups &= Q(create_date__year=datetime.now().year)

            order = form.data.get('order_by')

            return super().get_queryset().filter(
                lookups).select_related('category', 'author').order_by(
                order if order else 'pk')

        return super().get_queryset().select_related('category', 'author')


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    slug_url_kwarg = 'post_slug'
    template_name = 'feed/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'feed/add.html'
    extra_context = {'title': 'Add post'}

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(post.get_absolute_url())


class PostUpdateView(LoginRequiredMixin, PostAuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'feed/edit.html'
    context_object_name = 'post'
    extra_context = {'title': 'Edit post'}
    pk_url_kwarg = 'post_id'
    slug_url_kwarg = 'post_slug'


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
