from django.urls import path
from django.contrib.auth.views import logout_then_login

from users.views import (
    SignUpView,
    SignInView,
    PersonalSettingsView,
    SecuritySettingsView,
    UserEmailChangeView,
    UserPasswordChangeView,
    NotificationSettingsView,
)

app_name = 'users'

urlpatterns = [
    path('new/', SignUpView.as_view(), name='new'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('settings/personal/', PersonalSettingsView.as_view(), name='personal'),
    path('settings/security/', SecuritySettingsView.as_view(), name='security'),
    path('settings/security/email-change/', UserEmailChangeView.as_view(), name='email_change'),
    path('settings/security/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('settings/notifications/', NotificationSettingsView.as_view(), name='notifications'),
]
