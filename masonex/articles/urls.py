from django.urls import path

from .views import (
    ArticleListView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleUpdateView,
    AuthorDetailView,
    save_article_view,
    unsave_article_view,
    follow_author_view,
    unfollow_author_view,
    AuthorBookmarksView,
)

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('new/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/<slug:slug>/save/', save_article_view, name='article_save'),
    path('<int:pk>/<slug:slug>/unsave/', unsave_article_view, name='article_unsave'),
    path('bookmarks/', AuthorBookmarksView.as_view(), name='bookmarks'),
    path('authors/<str:username>/', AuthorDetailView.as_view(), name='author_detail'),
    path('authors/<str:username>/follow/', follow_author_view, name='follow_author'),
    path('authors/<str:username>/unfollow/', unfollow_author_view, name='unfollow_author'),
]
