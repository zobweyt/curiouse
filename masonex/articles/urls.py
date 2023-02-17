from django.urls import path

from .views import (
    ArticleListView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleUpdateView,
)

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('new/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article_update'),
]
