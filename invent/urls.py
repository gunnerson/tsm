from django.urls import path

from .views import (
    index,
    SummaryListView,
    TruckFormSetView,
    TrailerFormSetView,
    DriverFormSetView,
    TruckDetailView,
    TrailerDetailView,
    DriverDetailView,
)

app_name = "invent"

urlpatterns = [
    path('', index, name='index'),
    path('summary/', SummaryListView.as_view(
        template_name="invent/summary.html"),
        name='summary'),
    path('trucks/', TruckFormSetView.as_view(),
         name='list_trucks'),
    path('trailers/', TrailerFormSetView.as_view(),
         name='list_trailers'),
    path('drivers/', DriverFormSetView.as_view(),
         name='list_drivers'),
    path('truck/<int:pk>', TruckDetailView.as_view(
        template_name="invent/detail.html"),
        name='truck'),
    path('trailer/<int:pk>', TrailerDetailView.as_view(
        template_name="invent/detail.html"),
        name='trailer'),
    path('driver/<int:pk>', DriverDetailView.as_view(
        template_name="invent/detail.html"),
        name='driver'),
]
