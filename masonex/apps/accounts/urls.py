from django.urls import path

from accounts.views import (
    SignUpView,
    SignInView,
    logout_user_view,
    ProfileUpdateView,
    UserEmailChangeView,
    UserPasswordChangeView,
)

app_name = 'accounts'

urlpatterns = [
    path('create/', SignUpView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/change-email/', UserEmailChangeView.as_view(), name='email_change'),
    path('profile/change-password/', UserPasswordChangeView.as_view(), name='password_change'),
]
