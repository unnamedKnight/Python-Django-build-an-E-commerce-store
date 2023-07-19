from django.urls import path
from . import views


urlpatterns = [
    path("register", views.register, name="register"),
    path("email-verification/<str:uidb64>/<str:token>/", views.email_verification, name="email_verification"),
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
]
