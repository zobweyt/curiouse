from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

from core.utils import TitleMixin
from .models import User
from .mixins import RedirectAuthenticatedUsersMixin, ProfileUpdateMixin
from .forms import *


class SignUpView(RedirectAuthenticatedUsersMixin, TitleMixin, CreateView):
    form_class = SignUpForm
    template_name = 'users/form.html'
    title = 'Sign up'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class SignInView(RedirectAuthenticatedUsersMixin, TitleMixin, LoginView):
    form_class = SignInForm
    template_name = 'users/form.html'
    title = 'Sign in'    

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user_view(request):
    logout(request)
    return redirect('users:login')


class ProfileUpdateView(ProfileUpdateMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user

    def get_title(self):
        return 'Customize profile'


def user_avatar_delete_view(request):
    request.user.avatar.delete()
    messages.success(request, 'Your avatar has been deleted.')
    return redirect('users:profile')


class UserEmailChangeView(ProfileUpdateMixin, FormView):
    form_class = UserEmailChangeForm
    template_name = 'users/security.html'
    updating_object = 'email'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserPasswordChangeView(ProfileUpdateMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/security.html'
    updating_object = 'password'


__all__ = [
    'SignUpView',
    'SignInView',
    'logout_user_view',
    'ProfileUpdateView',
    'user_avatar_delete_view',
    'UserEmailChangeView',
    'UserPasswordChangeView',
]
