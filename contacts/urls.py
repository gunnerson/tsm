from django.urls import path

from .views import (
    DriverCreateView,
    DriverListView,
    DriverUpdateView,
    CompanyCreateView,
    CompanyListView,
    CompanyUpdateView,
)

app_name = "contacts"

urlpatterns = [
    path('drivers/create/', DriverCreateView.as_view(),
         name='create_driver'),
    path('drivers/list/', DriverListView.as_view(),
         name='list_drivers'),
    path('drivers/update/<int:pk>', DriverUpdateView.as_view(),
         name='update_driver'),
    path('companies/create/', CompanyCreateView.as_view(),
         name='create_company'),
    path('companies/list/', CompanyListView.as_view(),
         name='list_companies'),
    path('companies/update/<int:pk>', CompanyUpdateView.as_view(),
         name='update_company'),
]
