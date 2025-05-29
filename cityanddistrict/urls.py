from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("clubs/", include("clubs.urls"), name="clubs-urls"),
    path("contact/", include("contact.urls"), name="contact-urls"),
    path("user/", include("useraccounts.urls"), name="useraccounts-urls"),
    path("", include("home.urls"), name="home-urls"),
]
