from django.urls import path

from .decorators import require_article_author
from .views import *

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('new/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/<slug:slug>/edit/', require_article_author(ArticleUpdateView.as_view()), name='article_update'),
    path('<int:pk>/<slug:slug>/delete/', article_delete_view, name='article_delete'),
    path('authors/<str:username>/', AuthorArticleListView.as_view(), name='author_detail'),
    path('categories/<int:pk>/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]
