from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('articles/', include('articles.urls')),
    path('notifications/', include('notifications.urls')),
    path('',  RedirectView.as_view(pattern_name='articles:article-list', permanent=True), name='index'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('__debug__', include('debug_toolbar.urls')))
