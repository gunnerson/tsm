from django.urls import path

from .views import (
    OrderImageView,
    OrderImageListView,
    InspectionImageView,
    InspectionImageListView,
    TruckImageView,
    TruckImageListView,
    TrailerImageView,
    TrailerImageListView,
)

app_name = "docs"

urlpatterns = [
    path('orders/<int:pk>/upload_image/', OrderImageView.as_view(),
         name='order_image'),
    path('orders/<int:pk>/images/', OrderImageListView.as_view(),
         name='order_images'),
    path('inspections/<int:pk>/upload_image/', InspectionImageView.as_view(),
         name='inspection_image'),
    path('inspections/<int:pk>/images/', InspectionImageListView.as_view(),
         name='inspection_images'),
    path('trucks/<int:pk>/upload_image/', TruckImageView.as_view(),
         name='truck_image'),
    path('trucks/<int:pk>/images/', TruckImageListView.as_view(),
         name='truck_images'),
    path('trailers/<int:pk>/upload_image/', TrailerImageView.as_view(),
         name='trailer_image'),
    path('trailers/<int:pk>/images/', TrailerImageListView.as_view(),
         name='trailer_images'),
]
