from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

from core.utils import TitleMixin
from .models import User
from .mixins import RedirectAuthenticatedUsersMixin, ProfileUpdateMixin, ProfileSecurityUpdateMixin
from .forms import *


class SignUpView(RedirectAuthenticatedUsersMixin, TitleMixin, CreateView):
    form_class = SignUpForm
    template_name = 'accounts/register.html'
    title = 'Sign up'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class SignInView(RedirectAuthenticatedUsersMixin, TitleMixin, LoginView):
    form_class = SignInForm
    template_name = 'accounts/login.html'
    title = 'Sign in'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user_view(request):
    logout(request)
    return redirect('accounts:login')


class ProfileUpdateView(ProfileUpdateMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_object(self):
        return self.request.user

    def get_title(self):
        return 'Customize profile'


def user_avatar_delete_view(request):
    request.user.avatar.delete()
    messages.success(request, 'Your avatar has been successfully deleted.')
    return redirect('accounts:profile')


class UserEmailChangeView(ProfileSecurityUpdateMixin, FormView):
    form_class = UserEmailChangeForm
    updating_object = 'email'
    form_action_url = reverse_lazy('accounts:email_change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserPasswordChangeView(ProfileSecurityUpdateMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    updating_object = 'password'
    form_action_url = reverse_lazy('accounts:password_change')


__all__ = [
    'SignUpView',
    'SignInView',
    'logout_user_view',
    'ProfileUpdateView',
    'user_avatar_delete_view',
    'UserEmailChangeView',
    'UserPasswordChangeView',
]
