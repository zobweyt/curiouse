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
    Adds 'form_action_url' with title to the context and creates success message depending on 'updating_object'.
    """

    template_name = 'accounts/profile_update_security_form.html'
    success_url = reverse_lazy('accounts:profile')

    updating_object = 'profile'
    form_action_url = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = self.form_action_url
        return context

    def get_success_message(self, cleaned_data):
        return f'The {self.updating_object} has been successfully updated!'

    def get_title(self):
        return f'Change {self.updating_object}'


class ProfileSecurityUpdateMixin(ProfileUpdateMixin):
    """
    Changes the form width and adds back to main profile page button.
    """

    css_form_width_class = 'w-md-4'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'use_main_profile_page_button': True,
            'form_width': self.css_form_width_class,
        })
        return context
