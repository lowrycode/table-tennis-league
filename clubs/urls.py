from django.urls import path
from . import views


urlpatterns = [
    path("", views.clubs, name="clubs"),
    path("<int:club_id>/reviews/", views.club_reviews, name="club_reviews"),
    path(
        "admin-dashboard/",
        views.club_admin_dashboard,
        name="club_admin_dashboard",
    ),
    path(
        "info/update/",
        views.update_club_info,
        name="update_club_info",
    ),
    path(
        "info/delete/",
        views.delete_club_info,
        name="delete_club_info",
    ),
    path(
        "venue/assign/",
        views.assign_venue,
        name="assign_venue",
    ),
    path(
        "venue/create/",
        views.create_venue,
        name="create_venue",
    ),
    path(
        "venue/<int:venue_id>/delete/",
        views.delete_venue,
        name="delete_venue",
    ),
    path(
        "venue/<int:venue_id>/unassign/",
        views.unassign_venue,
        name="unassign_venue",
    ),
    path(
        "venue/<int:venue_id>/update/",
        views.update_venue_info,
        name="update_venue_info",
    ),
    path(
        "venue/<int:venue_id>/modal/",
        views.venue_modal,
        name="venue_modal",
    ),
]
