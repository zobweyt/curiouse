from .models import Notification


def new_notifications_processor(request):
    has_new_notifications = Notification.objects.filter(recipient=request.user.pk).exists()
    context = {
        'has_new_notifications': has_new_notifications
    }
    return context
