from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from core.utils import TitleMixin


class RedirectAuthenticatedUsersMixin:
    """
    Redirects the current user to 'fail_url' if authenticated.
    """

    fail_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.fail_url)
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateMixin(LoginRequiredMixin, SuccessMessageMixin, TitleMixin):
    """
    Adds title to the context and creates success message depending on 'updating_object'.
    """

    template_name = 'users/settings.html'
    success_url = reverse_lazy('users:profile')
    updating_object = 'profile'

    def get_success_message(self, cleaned_data):
        return f'The {self.updating_object} has been updated.'

    def get_title(self):
        return f'Change {self.updating_object}'
