from django.urls import path

from feed.views import *

urlpatterns = [
    path('', PostListingView.as_view(), name='home'),
    path('accounts/create/', UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', UserAuthenticiationView.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path('settings/', UserSettingsView.as_view(), name='profile'),
    path('settings/change-email/', UserEmailChangeView.as_view(), name='email_change'),
    path('settings/change-password/', UserPasswordChangeView.as_view(), name='password_change'),
    path('articles/authors/<str:username>/', AuthorDetailView.as_view(), name='user'),
    path('articles/new/', PostCreateView.as_view(), name='post_create'),
    path('articles/search/', PostSearchView.as_view(), name='search'),
    path('articles/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('articles/<int:post_id>/<slug:post_slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('articles/<int:post_id>/<slug:post_slug>/delete/', post_delete, name='post_delete'),
    path('articles/categories/<slug:category_slug>/', CategoryView.as_view(), name='category'),
]
