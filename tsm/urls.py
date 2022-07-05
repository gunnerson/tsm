"""tsm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from .views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('users.urls'), name='users'),
    path('', include('invent.urls'), name='invent'),
    path('', include('shop.urls'), name='shop'),
    path('', include('docs.urls'), name='docs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler403 = 'tsm.views.permission_denied_view'
