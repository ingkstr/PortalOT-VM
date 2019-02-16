"""Listado general de urls"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('only_it_admin/', admin.site.urls),
    path('', include (('ordenes.urls','ordenes'),namespace='ordenes')),
]
