from django.urls import path
from . import views


urlpatterns = [
    path('account-settings/', views.account_settings, name="account_settings"),
    path('change-email/', views.change_email, name="change_email"),
]
