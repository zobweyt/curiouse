from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.conf import settings

from core.utils import TitleMixin


class RedirectAuthenticatedUsersMixin:
    """
    Redirects the request user to `settings.LOGIN_REDIRECT_URL` if authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class AuthMixin(RedirectAuthenticatedUsersMixin, TitleMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_button_text'] = self.get_title()
        return context


class SettingsMixin(LoginRequiredMixin, SuccessMessageMixin, TitleMixin):
    """
    Adds title to the context and creates success message depending on `updating_object`.
    """

    template_name = 'users/settings.html'
    success_url = reverse_lazy('users:personal')
    updating_object_name = 'profile'
    extra_context = {'submit_button_text': 'Save'}
    
    def get_object(self):
        return self.request.user
    
    def get_success_message(self, cleaned_data):
        return f'The {self.updating_object_name} has been updated.'

    def get_title(self):
        return f'Change {self.updating_object_name}'


class SecurityMixin(SettingsMixin):
    success_url = reverse_lazy('users:security')
