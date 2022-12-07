from django.urls import path

from articles.views import *

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('authors/<str:username>/', AuthorArticleListView.as_view(), name='user'),
    path('new/', ArticleCreateView.as_view(), name='article_create'),
    path('search/', ArticleSearchView.as_view(), name='search'),
    path('<int:article_pk>/<slug:article_slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:article_pk>/<slug:article_slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('<int:article_pk>/<slug:article_slug>/delete/', article_delete, name='article_delete'),
    path('categories/<slug:category_slug>/', ArticleCategoryListView.as_view(), name='category'),
]
