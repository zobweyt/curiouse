from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from core.decorators import require_htmx
from .models import Notification


@method_decorator(require_htmx, name='dispatch')
class NotificationsListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notifications/notification-list.html'
    paginate_by = 8
    allow_empty = True
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'actor',
            'action_object_content_type',
            'target_content_type'
        ).filter(
            recipient=self.request.user
        )
        return queryset


@require_htmx
@login_required
def delete_notification_view(request, pk):
    notifications = Notification.objects.filter(recipient=request.user)
    get_object_or_404(notifications, pk=pk, recipient=request.user).delete()
    
    if not notifications:
        template_name = 'notifications/notification-list.html'
    else:
        template_name = 'notifications/notification.html'
            
    return render(request, template_name)


@require_htmx
@login_required
def delete_all_notifications_view(request):
    Notification.objects.filter(recipient=request.user).delete()    
    return render(request, 'notifications/notification-list.html')
