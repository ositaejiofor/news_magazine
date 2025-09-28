from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view
from dashboard.views import dashboard_view
from .views import login_view, logout_view, profile_view
from dashboard.views import dashboard_view





from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),

    # Register
    path("register/", views.register_view, name="register"),

    # Profile
    path("profile/", views.profile_view, name="profile"),

    path("dashboard/", dashboard_view, name="dashboard"),  # superuser only


    # Change password
    path("password-change/", views.change_password_view, name="change_password"),

    # Password reset (Django built-in)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
