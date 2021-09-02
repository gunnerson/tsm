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
    TruckDocumentView,
    TruckDocumentListView,
    TrailerDocumentView,
    TrailerDocumentListView,
    DriverDocumentView,
    DriverDocumentListView,
    CompanyDocumentView,
    CompanyDocumentListView,
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
    path('trucks/<int:pk>/upload_document/', TruckDocumentView.as_view(),
         name='truck_doc'),
    path('trucks/<int:pk>/documents/', TruckDocumentListView.as_view(),
         name='truck_files'),
    path('trailers/<int:pk>/upload_document/', TrailerDocumentView.as_view(),
         name='trailer_doc'),
    path('trailers/<int:pk>/documents/', TrailerDocumentListView.as_view(),
         name='trailer_files'),
    path('drivers/<int:pk>/upload_document/', DriverDocumentView.as_view(),
         name='driver_doc'),
    path('drivers/<int:pk>/documents/', DriverDocumentListView.as_view(),
         name='driver_files'),
    path('companies/<int:pk>/upload_document/', CompanyDocumentView.as_view(),
         name='company_doc'),
    path('companies/<int:pk>/documents/', CompanyDocumentListView.as_view(),
         name='company_files'),
]