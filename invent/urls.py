from django.urls import path

from . import views

app_name = "invent"

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/', views.SummaryListView.as_view(
        template_name="invent/summary.html"),
        name='summary'),
    # path('trucks/list/', views.trucks_list_view,
    #      name='list_trucks'),
    path('trucks/list/', views.TruckFormSetView.as_view(),
         name='list_trucks'),
    path('trailers/list/', views.TrailerFormSetView.as_view(),
         name='list_trailers'),
    path('truck/<int:pk>', views.TruckDetailView.as_view(
        template_name="invent/detail.html"),
        name='truck'),
    path('trailer/<int:pk>', views.TrailerDetailView.as_view(
        template_name="invent/detail.html"),
        name='trailer'),
]
