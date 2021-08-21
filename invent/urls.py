from django.urls import path

from .views import (
    index,
    SummaryListView,
    TruckFormSetView,
    TrailerFormSetView,
    TruckDetailView,
    TrailerDetailView,
)

app_name = "invent"

urlpatterns = [
    path('', index, name='index'),
    path('summary/', SummaryListView.as_view(
        template_name="invent/summary.html"),
        name='summary'),
    path('trucks/list/', TruckFormSetView.as_view(),
         name='list_trucks'),
    path('trailers/list/', TrailerFormSetView.as_view(),
         name='list_trailers'),
    path('truck/<int:pk>', TruckDetailView.as_view(
        template_name="invent/detail.html"),
        name='truck'),
    path('trailer/<int:pk>', TrailerDetailView.as_view(
        template_name="invent/detail.html"),
        name='trailer'),
]
