"""tsm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls'), name='users'),
    path('', include('invent.urls'), name='invent'),
]

handler403 = 'invent.views.permission_denied_view'
