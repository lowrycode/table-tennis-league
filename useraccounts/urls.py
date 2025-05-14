from django.urls import path
from . import views


urlpatterns = [
    path("account/settings/", views.account_settings, name="account_settings"),
    path("account/email/change/", views.change_email, name="change_email"),
    path(
        "account/delete/confirm/", views.delete_account, name="delete_account"
    ),
]
