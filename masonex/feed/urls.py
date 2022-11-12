from django.urls import path

from feed.views import (
    HomeView,
    CategoryView,
    SearchView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    UserAuthenticiationView,
    UserRegistrationView,
    UserProfileView,
    UserPasswordChangeView,
    UserEmailChangeView,
    logout_user,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('search/', SearchView.as_view(), name='search'),
    path('post/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/', PostDetailView.as_view()),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('edit/<int:post_id>/<slug:post_slug>/', PostUpdateView.as_view(), name='post_update'),
    path('edit/<int:post_id>/', PostUpdateView.as_view()),
    path('login/', UserAuthenticiationView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('email-change/', UserEmailChangeView.as_view(), name='email_change'),
    path('logout/', logout_user, name='logout'),
]
