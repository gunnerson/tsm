from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .utils import generate_profile

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name="login"),
    path('logout/', LogoutView.as_view(next_page='invent:index'),
         name="logout"),
    path('register/', views.register, name="register"),
    path('password/', views.change_password, name="change_password"),
    path('generate_profile/', generate_profile, name="generate_profile"),
    path('generate_profile/', generate_profile, name="generate_profile"),
    path('settings/<int:pk>', views.PreferenceListUpdateView.as_view(
        template_name='users/preferences.html'),
        name="preferences"),
    path('settings/table_columns', views.ListColShowListView.as_view(
        template_name='users/listcolshow.html'),
        name="listcolshow"),
]
