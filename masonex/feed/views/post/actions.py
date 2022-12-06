from hitcount.views import HitCountDetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView

from .mixins import AuthorRequiredMixin, PostMixin
from feed.forms import PostForm
from feed.models import Post


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'feed/post_editor.html'
    extra_context = {'title': 'Create post'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit'] = 'Publish'
        context['action'] = reverse_lazy('post_create')
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(post.get_absolute_url())


class PostDetailView(PostMixin, HitCountDetailView):
    template_name = 'feed/post_detail.html'
    count_hit = True
    

class PostUpdateView(AuthorRequiredMixin, PostMixin, UpdateView):
    form_class = PostForm
    template_name = 'feed/post_editor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['submit'] = 'Edit'
        context['action'] = reverse_lazy('post_update', kwargs={
            self.pk_url_kwarg: post.pk, self.slug_url_kwarg: post.slug
        })
        return context


def post_delete(request, post_id, post_slug):
    get_object_or_404(Post, pk=post_id, slug=post_slug).delete()
    return redirect('home')
