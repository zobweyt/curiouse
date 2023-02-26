from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .models import Notification


class NotificationsListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notifications/items.html'
    paginate_by = 8
    allow_empty = True
    
    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
      
    def get_queryset(self):
        return super().get_queryset().select_related('recipient', 'sender').filter(recipient=self.request.user)


@login_required
def delete(request, pk):
    notifications = Notification.objects.filter(recipient=request.user)
    get_object_or_404(notifications, pk=pk, recipient=request.user).delete()
        
    if request.htmx:
        if notifications.count() == 0:
            template_name = 'notifications/items.html'
        else:
            template_name = 'notifications/item.html'
            
        return render(request, template_name)
    
    return redirect('index')


@login_required
def delete_all(request):
    Notification.objects.filter(recipient=request.user).delete()
    
    if request.htmx:
        return render(request, 'notifications/items.html')
    return redirect('index')
