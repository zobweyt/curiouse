from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class ExcludeAuthenticatedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
            
        return super().dispatch(request, *args, **kwargs)


class SettingsAuthUpdateMixin(LoginRequiredMixin, SuccessMessageMixin):
    template_name = 'feed/settings_auth_update_form.html'
    success_url = reverse_lazy('profile')

    def __init__(self):
        super().__init__()
        self.success_message = f'The {self.updating_object} has been successfully changed!'
        self.extra_context = {
            'title': f'{str.capitalize(self.updating_object)} change',
            'action': reverse_lazy(f'{self.updating_object}_change')
        }
