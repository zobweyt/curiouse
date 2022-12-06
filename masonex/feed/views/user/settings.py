from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView

from feed.forms import ProfileForm, UserPasswordChangeForm, UserEmailChangeForm
from feed.models import User


class UserSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'feed/profile_update.html'
    extra_context = {'title': 'Profile'}
    success_message = 'The profile has been successfully updated!'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


class UserEmailChangeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = UserEmailChangeForm
    template_name = 'feed/profile_auth_update_form.html'
    success_url = reverse_lazy('profile')
    success_message = 'The email has been successfully changed!'
    extra_context = {
        'title': 'Change email',
        'action': reverse_lazy('email_change')
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'feed/profile_auth_update_form.html'
    success_url = reverse_lazy('profile')
    success_message = 'The password has been successfully changed!'
    extra_context = {
        'title': 'Change password',
        'action': reverse_lazy('password_change')
    }
