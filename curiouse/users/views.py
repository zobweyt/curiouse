from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, TemplateView

from core.utils import TitleMixin
from .models import User
from .mixins import AuthMixin, SettingsMixin, SecurityMixin
from .forms import (
    SignInForm,
    SignUpForm,
    ProfileUpdateForm,
    UserEmailChangeForm,
    UserPasswordChangeForm,
)


class SignUpView(AuthMixin, CreateView):
    form_class = SignUpForm
    template_name = 'users/form.html'
    title = 'Sign up'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class SignInView(AuthMixin, LoginView):
    form_class = SignInForm
    template_name = 'users/form.html'
    title = 'Sign in'


class PersonalSettingsView(SettingsMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/personal.html'


class SecuritySettingsView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = 'users/security.html'
    title = 'Security'


class UserEmailChangeView(SecurityMixin, FormView):
    form_class = UserEmailChangeForm
    updating_object_name = 'email'

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        return super().form_valid(form)


class UserPasswordChangeView(SecurityMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    updating_object_name = 'password'
    
    
class NotificationSettingsView(SettingsMixin, UpdateView):
    model = User
    fields = ('new_follow_notifications', 'new_article_notifications')
    template_name = 'users/notifications.html'
    success_url = reverse_lazy('users:notifications')
    updating_object_name = 'notifications'
