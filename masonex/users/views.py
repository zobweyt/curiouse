from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, FormView, TemplateView

from core.utils import TitleMixin
from .models import User
from .mixins import RedirectAuthenticatedUsersMixin, SettingsMixin
from .forms import (
    SignInForm,
    SignUpForm,
    ProfileUpdateForm,
    UserEmailChangeForm,
    UserPasswordChangeForm
)


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


class PersonalSettingsView(SettingsMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/personal.html'

    def get_object(self):
        return self.request.user

    def get_title(self):
        return 'Personal'
    

def user_avatar_delete_view(request):
    request.user.avatar.delete()
    messages.success(request, 'Your avatar has been deleted.')
    return redirect('users:personal')


class SecuritySettingsView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = 'users/security.html'
    title = 'Security'


class UserEmailChangeView(SettingsMixin, FormView):
    form_class = UserEmailChangeForm
    updating_object = 'email'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserPasswordChangeView(SettingsMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    updating_object = 'password'
