from django.urls import path
from . import views


urlpatterns = [
    path("register", views.register, name="register"),
    # email-verification urls
    path(
        "email-verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email_verification",
    ),
    path(
        "email-verification-sent",
        views.email_verification_sent,
        name="email_verification_sent",
    ),
    path(
        "email-verification-success",
        views.email_verification_success,
        name="email_verification_success",
    ),
    path(
        "email-verification-failed",
        views.email_verification_failed,
        name="email_verification_failed",
    ),
    # login-logout urls
    path("login/", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    # account delete and profile management
    path("profile-management", views.profile_management, name="profile_management"),
    path("delete-account", views.delete_account, name="delete_account"),
]
