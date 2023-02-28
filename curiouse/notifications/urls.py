from django.urls import path

from .views import (
    NotificationsListView,
    delete,
    delete_all,
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications-list'),
    path('<int:pk>/delete', delete, name='delete'),
    path('delete_all', delete_all, name='delete_all'),
]
