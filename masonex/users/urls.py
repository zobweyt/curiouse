from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('new/', SignUpView.as_view(), name='new'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('settings/personal/', PersonalSettingsView.as_view(), name='profile'),
    path('settings/personal/avatar-delete/', user_avatar_delete_view, name='user_avatar_delete'),
    path('settings/security/', security_settings_view, name='security'),
    path('settings/security/email-change/', UserEmailChangeView.as_view(), name='email_change'),
    path('settings/security/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
]
