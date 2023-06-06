from django.urls import path
from django.contrib.auth.views import logout_then_login

from users import views

app_name = 'users'

urlpatterns = [
    path('new/', views.SignUpView.as_view(), name='new'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('settings/personal/', views.PersonalSettingsView.as_view(), name='personal'),
    path('settings/security/', views.SecuritySettingsView.as_view(), name='security'),
    path('settings/security/email-change/', views.UserEmailChangeView.as_view(), name='email_change'),
    path('settings/security/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('settings/notifications/', views.NotificationSettingsView.as_view(), name='notifications'),
]
