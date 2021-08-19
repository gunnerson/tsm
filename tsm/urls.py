"""tsm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trucking/', include('users.urls'), name='users'),
    path('trucking/', include('contacts.urls'), name='contacts'),
    path('trucking/', include('invent.urls'), name='invent'),
]
