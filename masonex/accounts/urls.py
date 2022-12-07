from django.urls import path

from accounts.views import *

urlpatterns = [
    path('create/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserAuthenticiationView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('settings/', UserSettingsView.as_view(), name='profile'),
    path('settings/change-email/', UserEmailChangeView.as_view(), name='email_change'),
    path('settings/change-password/', UserPasswordChangeView.as_view(), name='password_change'),
]
