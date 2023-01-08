from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('new/', SignUpView.as_view(), name='new'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/delete-avatar/', user_avatar_delete_view, name='user_avatar_delete'),
    path('profile/change-email/', UserEmailChangeView.as_view(), name='email_change'),
    path('profile/change-password/', UserPasswordChangeView.as_view(), name='password_change'),
]
