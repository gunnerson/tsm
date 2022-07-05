from django.urls import path

from .views import (
    summary,
    TruckFormSetView,
    TrailerFormSetView,
    CompanyFormSetView,
    TruckDetailView,
    TrailerDetailView,
    CompanyDetailView,
    MapView,
)

from .gomotive import (
    # get_bulk_vehicles_locations,
    gomotive_webhook,
)


app_name = "invent"

urlpatterns = [
    path('summary/', summary, name='summary'),
    path('map/', MapView.as_view(), name='map'),
    # path('api/summary/get_vehicles_locations/',
    #      get_bulk_vehicles_locations, name='get_vehicles_locations'),
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
    path('webhook/gomotive/', gomotive_webhook, name='gomotive_webhook'),
]
