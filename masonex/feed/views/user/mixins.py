from django.shortcuts import redirect


class ExcludeAuthenticatedUsersMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
