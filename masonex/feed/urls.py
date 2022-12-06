from django.urls import path

from feed.views import *

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('accounts/create/', UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', UserAuthenticiationView.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path('settings/', UserSettingsView.as_view(), name='profile'),
    path('settings/change-email/', UserEmailChangeView.as_view(), name='email_change'),
    path('settings/change-password/', UserPasswordChangeView.as_view(), name='password_change'),
    path('articles/authors/<str:username>/', AuthorArticleListView.as_view(), name='user'),
    path('articles/new/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/search/', ArticleSearchView.as_view(), name='search'),
    path('articles/<int:article_pk>/<slug:article_slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:article_pk>/<slug:article_slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<int:article_pk>/<slug:article_slug>/delete/', article_delete, name='article_delete'),
    path('articles/categories/<slug:category_slug>/', ArticleCategoryListView.as_view(), name='category'),
]
