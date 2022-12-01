from django.contrib import admin
from django.urls import path, include

from masonex import settings
from feed.views import handle_page_not_found, handle_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('', include('feed.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    urlpatterns.append(path('__debug__', include('debug_toolbar.urls')))

handler404 = handle_page_not_found
handler500 = handle_server_error
