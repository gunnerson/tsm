from django.urls import path

from .views import (
    index,
    summary,
    TruckFormSetView,
    TrailerFormSetView,
    DriverFormSetView,
    CompanyFormSetView,
    TruckDetailView,
    TrailerDetailView,
    DriverDetailView,
    CompanyDetailView,
)

app_name = "invent"

urlpatterns = [
    path('', index, name='index'),
    path('summary/', summary, name='summary'),
    path('trucks/', TruckFormSetView.as_view(),
         name='list_trucks'),
    path('trailers/', TrailerFormSetView.as_view(),
         name='list_trailers'),
    path('drivers/', DriverFormSetView.as_view(),
         name='list_drivers'),
    path('companies/', CompanyFormSetView.as_view(),
         name='list_companies'),
    path('truck/<int:pk>', TruckDetailView.as_view(
        template_name="invent/detail.html"),
        name='truck'),
    path('trailer/<int:pk>', TrailerDetailView.as_view(
        template_name="invent/detail.html"),
        name='trailer'),
    path('driver/<int:pk>', DriverDetailView.as_view(
        template_name="invent/detail.html"),
        name='driver'),
    path('company/<int:pk>', CompanyDetailView.as_view(
        template_name="invent/detail.html"),
        name='company'),
]
