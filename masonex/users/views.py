from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, View

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


def logout_user_view(request):
    logout(request)
    return redirect('users:login')


class PersonalSettingsView(ProfileUpdateMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/personal.html"

    def get_object(self):
        return self.request.user

    def get_title(self):
        return 'Personal'
    

@login_required
def security_settings_view(request):
    return render(request, "users/security.html", {"title": "Security"})


def user_avatar_delete_view(request):
    request.user.avatar.delete()
    messages.success(request, 'Your avatar has been deleted.')
    return redirect('users:profile')


class UserEmailChangeView(ProfileUpdateMixin, FormView):
    form_class = UserEmailChangeForm
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
    updating_object = 'password'


__all__ = [
    'SignUpView',
    'SignInView',
    'logout_user_view',
    'PersonalSettingsView',
    'security_settings_view',
    'user_avatar_delete_view',
    'UserEmailChangeView',
    'UserPasswordChangeView',
]
