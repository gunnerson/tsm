from django.urls import path

from .views import (
    index,
    SummaryListView,
    TruckCreateView,
    trucks_list_view,
    TruckUpdateView,
    TrailerCreateView,
    trailers_list_view,
    TrailerUpdateView,
)

app_name = "invent"

urlpatterns = [
    path('', index, name='index'),
    path('trucks/create/', TruckCreateView.as_view(
        template_name="invent/create_form.html"),
        name='create_truck'),
    path('trucks/list/', trucks_list_view,
         name='list_trucks'),
    # path('summary/', summary_view, name='summary'),
    path('summary/', SummaryListView.as_view(
        template_name="invent/summary.html"),
        name='summary'),
    path('trucks/update/<int:pk>', TruckUpdateView.as_view(
        template_name="invent/update_form.html"),
        name='update_truck'),
    path('trailers/create/', TrailerCreateView.as_view(
        template_name="invent/create_form.html"),
        name='create_trailer'),
    path('trailers/list/', trailers_list_view,
         name='list_trailers'),
    path('trailers/update/<int:pk>', TrailerUpdateView.as_view(
        template_name="invent/update_form.html"),
        name='update_trailer'),
]
