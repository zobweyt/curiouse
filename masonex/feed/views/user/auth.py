from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .utils import ExcludeAuthenticatedUsersMixin
from feed.forms import UserRegistrationForm, UserAuthenticiationForm


class UserRegistrationView(ExcludeAuthenticatedUsersMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'feed/auth/register.html'
    extra_context = {'title': 'Sign up'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home') 


class UserAuthenticiationView(ExcludeAuthenticatedUsersMixin, LoginView):
    form_class = UserAuthenticiationForm
    template_name = 'feed/auth/login.html'
    extra_context = {'title': 'Sign in'}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
