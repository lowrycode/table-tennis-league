from django.urls import path
from . import views


urlpatterns = [
    path('', views.clubs, name="clubs"),
    path('admin-dashboard', views.club_admin_dashboard, name="club_admin_dashboard"),
]
