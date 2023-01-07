from django.urls import path
from django.views.generic.base import RedirectView

from articles.views import *

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('authors/<str:username>/', AuthorArticleListView.as_view(), name='user'),
    path('new/', ArticleCreateView.as_view(), name='article_create'),
    path('search/', ArticleSearchView.as_view(), name='search'),
    path('categories/<int:pk>/<slug:slug>/', RedirectView.as_view(pattern_name='articles:home', permanent=False), name='category'), # create view to categories
    path('<int:article_pk>/<slug:article_slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:article_pk>/<slug:article_slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('<int:article_pk>/<slug:article_slug>/delete/', article_delete, name='article_delete'),
]
