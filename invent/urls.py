from django.urls import path

from .views import (
    summary,
    TruckFormSetView,
    TrailerFormSetView,
    CompanyFormSetView,
    TruckDetailView,
    TrailerDetailView,
    CompanyDetailView,
)

app_name = "invent"

urlpatterns = [
    path('summary/', summary, name='summary'),
    path('trucks/', TruckFormSetView.as_view(),
         name='list_trucks'),
    path('trailers/', TrailerFormSetView.as_view(),
         name='list_trailers'),
    path('companies/', CompanyFormSetView.as_view(),
         name='list_companies'),
    path('truck/<int:pk>/', TruckDetailView.as_view(
        template_name="invent/detail.html"),
        name='truck'),
    path('trailer/<int:pk>/', TrailerDetailView.as_view(
        template_name="invent/detail.html"),
        name='trailer'),
    path('company/<int:pk>/', CompanyDetailView.as_view(
        template_name="invent/detail.html"),
        name='company'),
]
