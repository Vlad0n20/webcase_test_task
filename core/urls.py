from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from core.yasg import urlpatterns as doc_urls
from apps.urls import urlpatterns as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.jwt')),
]
urlpatterns += doc_urls
urlpatterns += app_urls

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
