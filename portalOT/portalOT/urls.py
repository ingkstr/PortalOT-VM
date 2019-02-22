"""Listado general de urls"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('only_it_admin/', admin.site.urls),
    path('', include (('ordenes.urls','ordenes'),namespace='ordenes')),
]  + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
