from django.urls import path

from .views import (
    index,
    TruckCreateView,
    TruckListView,
    TruckDetailView,
    TruckUpdateView,
)

app_name = "invent"

urlpatterns = [
    path('', index, name='index'),
    path('inventory/trucks/create/', TruckCreateView.as_view(),
         name='create_truck'),
    path('inventory/trucks/list/', TruckListView.as_view(),
         name='list_trucks'),
    path('inventory/trucks/detail/<int:pk>', TruckDetailView.as_view(),
         name='truck_detail'),
    path('inventory/trucks/update/<int:pk>', TruckUpdateView.as_view(),
         name='update_truck'),
]
