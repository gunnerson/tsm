from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserLoginForm
from .utils import generate_su_profile
from .views import (
    register,
    ProfileUpdateView,
    ListColShowListView,
    UsersLevelFormSetView,
    punch,
    PunchCardListView,
)

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        authentication_form=UserLoginForm),
        name="login"),
    path('logout/', LogoutView.as_view(next_page='index'),
         name="logout"),
    path('register/', register, name="register"),
    path('generate_profile/', generate_su_profile, name="generate_su_profile"),
    path('settings/<int:pk>/', ProfileUpdateView.as_view(
        template_name='users/preferences.html'),
        name="profile"),
    path('columns/', ListColShowListView.as_view(
        template_name='users/listcolshow.html'),
        name="listcolshow"),
    path('access/', UsersLevelFormSetView.as_view(),
         name="update_level"),
    path('punch/', punch, name="punch"),
    path('hours/', PunchCardListView.as_view(), name="hours"),
]
