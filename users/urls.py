from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm, UserChangeForm
from .utils import generate_su_profile
from . import views

app_name = "users"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=UserLoginForm),
        name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'),
         name="logout"),
    path('register/', views.register, name="register"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="users/password_reset.html",
        form_class=UserChangeForm,
        success_url=reverse_lazy('users:password_reset_done'),
        email_template_name="users/password_reset_email.html"),
        name="reset_password"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy('users:password_reset_complete')),
        name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"),
        name="password_reset_complete"),
    path('generate_profile/', generate_su_profile,
         name="generate_su_profile"),
    path('settings/<int:pk>/', views.ProfileUpdateView.as_view(
        template_name='users/preferences.html'),
        name="profile"),
    path('columns/', views.ListColShowListView.as_view(
        template_name='users/listcolshow.html'),
        name="listcolshow"),
    path('access/', views.UsersLevelFormSetView.as_view(),
         name="update_level"),
    path('account/', views.AccountvarFormSetView.as_view(),
         name="update_account"),
    path('punch/', views.punch, name="punch"),
    path('hours/', views.PunchCardListView.as_view(), name="hours"),
]
