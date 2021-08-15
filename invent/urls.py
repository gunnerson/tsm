from django.urls import path

from .views import (
    index,
    TruckCreateView,
    TruckListView,
    TruckUpdateView,
    TrailerCreateView,
    TrailerListView,
    TrailerUpdateView,
)

app_name = "invent"

urlpatterns = [
    path('', index, name='index'),
    path('trucks/create/', TruckCreateView.as_view(
        template_name="invent/create_form.html"),
        name='create_truck'),
    path('trucks/list/', TruckListView.as_view(),
         name='list_trucks'),
    path('trucks/update/<int:pk>', TruckUpdateView.as_view(
        template_name="invent/update_form.html"),
        name='update_truck'),
    path('trailers/create/', TrailerCreateView.as_view(
        template_name="invent/create_form.html"),
        name='create_trailer'),
    path('trailers/list/', TrailerListView.as_view(),
         name='list_trailers'),
    path('trailers/update/<int:pk>', TrailerUpdateView.as_view(
        template_name="invent/update_form.html"),
        name='update_trailer'),
]
