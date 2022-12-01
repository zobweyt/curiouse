from django.urls import path

from feed.views import (
    HomeView,
    CategoryView,
    SearchView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    post_delete,
    UserAuthenticiationView,
    UserRegistrationView,
    UserProfileView,
    UserPasswordChangeView,
    UserEmailChangeView,
    AuthorDetailView,
    logout_user,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('search/', SearchView.as_view(), name='search'),
    path('post/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/', PostDetailView.as_view()),
    path('create-post/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:post_id>/<slug:post_slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:post_id>/edit/', PostUpdateView.as_view()),
    path('login/', UserAuthenticiationView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('profile/email-change/', UserEmailChangeView.as_view(), name='email_change'),
    path('user/<str:username>/', AuthorDetailView.as_view(), name='user'),
    path('logout/', logout_user, name='logout'),
    path('post/<int:post_id>/<slug:post_slug>/delete/', post_delete, name='post_delete'),
    path('post/<int:post_id>/delete/',post_delete),
]
