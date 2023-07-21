from django.urls import path
from django.contrib.auth import views as auth_views
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
    # Password management urls/views
    # 1 ) Submit our email form
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password-reset.html"
        ),
        name="reset_password",
    ),
    # 2) Success message stating that a password reset email was sent
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    # 3) Password reset link
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    # 4) Success message stating that our password was reset
    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),

    # manage shipping
    path('manage-shipping', views.manage_shipping, name='manage_shipping'),
]
