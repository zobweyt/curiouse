from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView

from .utils import SettingsAuthUpdateMixin
from feed.forms import ProfileForm, UserEmailChangeForm, UserPasswordChangeForm
from feed.models import User


class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'feed/settings_update.html'
    success_message = 'The profile has been successfully updated!'
    extra_context = {'title': 'Profile'}

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


class UserEmailChangeView(SettingsAuthUpdateMixin, FormView):
    form_class = UserEmailChangeForm
    updating_object = 'email'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserPasswordChangeView(SettingsAuthUpdateMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    updating_object = 'password'
