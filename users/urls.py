from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserLoginForm
from .utils import generate_su_profile
from .views import (
    register,
    PreferenceListUpdateView,
    ListColShowListView,
    UsersLevelFormSetView,
)

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        authentication_form=UserLoginForm),
        name="login"),
    path('logout/', LogoutView.as_view(next_page='invent:index'),
         name="logout"),
    path('register/', register, name="register"),
    path('generate_profile/', generate_su_profile, name="generate_su_profile"),
    path('user/settings/<int:pk>', PreferenceListUpdateView.as_view(
        template_name='users/preferences.html'),
        name="preferences"),
    path('user/settings/table_columns', ListColShowListView.as_view(
        template_name='users/listcolshow.html'),
        name="listcolshow"),
    path('account/users/', UsersLevelFormSetView.as_view(),
         name="update_level"),
]
