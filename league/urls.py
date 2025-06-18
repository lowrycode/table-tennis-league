from django.urls import path
from . import views


urlpatterns = [
    path("fixtures/", views.fixtures, name="fixtures"),
    path("fixtures/filter", views.fixtures_filter, name="fixtures_filter"),
    path("results/", views.results, name="results"),
]
