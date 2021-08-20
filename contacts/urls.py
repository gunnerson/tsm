from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path('drivers/create/', views.DriverCreateView.as_view(),
         name='create_driver'),
    path('drivers/list/', views.drivers_list_view,
         name='list_drivers'),
    path('drivers/update/<int:pk>', views.DriverUpdateView.as_view(),
         name='update_driver'),
    path('companies/create/', views.CompanyCreateView.as_view(),
         name='create_company'),
    path('companies/list/', views.CompanyListView.as_view(),
         name='list_companies'),
    path('companies/update/<int:pk>', views.CompanyUpdateView.as_view(),
         name='update_company'),
    path('passwords/group/create/', views.PasswordGroupCreateView.as_view(),
         name='create_password_group'),
    path('passwords/list/', views.DriverListView.as_view(),
         name='list_passwords'),
]
