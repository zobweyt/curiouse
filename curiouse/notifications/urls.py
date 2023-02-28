from django.urls import path

from .views import (
    delete_all_notifications_view,
    delete_notification_view,
    NotificationsListView,
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications-list'),
    path('delete_all', delete_all_notifications_view, name='delete_all'),
    path('<int:pk>/delete', delete_notification_view, name='delete'),
]
