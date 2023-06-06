from django.urls import path

from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('bookmarks/', views.AuthorBookmarksView.as_view(), name='author-bookmarks-list'),
    path('subscriptions/', views.AuthorSubscriptionsView.as_view(), name='author-subscriptions-list'),
    path('new/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/<slug:slug>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/<slug:slug>/save/', views.save_article_view, name='article_save'),
    path('<int:pk>/<slug:slug>/unsave/', views.unsave_article_view, name='article_unsave'),
    path('authors/<str:username>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/<str:username>/follow/', views.follow_author_view, name='follow_author'),
    path('authors/<str:username>/unfollow/', views.unfollow_author_view, name='unfollow_author'),
]
