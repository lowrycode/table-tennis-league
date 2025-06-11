from django.http import HttpResponseBadRequest
from django.db.models import Prefetch
from django.shortcuts import render
from .models import Week, Fixture
from .filters import FixtureFilter


def fixtures(request):
    # Get fixtures with attached data
    all_fixtures = Fixture.objects.select_related("season", "division").all()

    # Apply filter
    fixture_filter = FixtureFilter(request.GET, queryset=all_fixtures)
    filtered_fixtures_qs = fixture_filter.qs

    # Get season from bound form - defaults to current season or None
    season = fixture_filter.form.cleaned_data.get("season")

    # Get season_weeks
    if season:
        season_week_ids = (
            Week.objects.filter(season=season)
            .order_by("start_date")
            .values_list("id", flat=True)
        )

        season_weeks = (
            Week.objects.filter(id__in=season_week_ids)
            .prefetch_related(
                Prefetch("week_fixtures", queryset=filtered_fixtures_qs)
            )
            .order_by("start_date")
        )
    else:
        season_weeks = None

    # Used for the fixture status colour key (format: CSS class, label)
    fixture_status_key = [
        ("fixture-scheduled", "Scheduled"),
        ("fixture-completed", "Completed"),
        ("fixture-postponed", "Postponed"),
        ("fixture-cancelled", "Cancelled"),
    ]

    # Deduce whether filters are applied by checking for get parameters
    filters_applied = len(request.GET) > 0

    # Build context
    context = {
        "season": season,
        "weeks": season_weeks,
        "fixture_status_key": fixture_status_key,
        "filter": fixture_filter,
        "filters_applied": filters_applied,
    }

    # If htmx request, return only the fixtures_section partial template
    if request.headers.get("HX-Request") == "true":
        return render(
            request, "league/partials/fixtures_section.html", context
        )

    return render(request, "league/fixtures.html", context)


def fixtures_filter(request):
    """
    Render the fixtures_filter_panel_inner partial with filter form contents.

    This allows for dynamically updating dropdown options via HTMX.
    """
    # If not HTMX request, return error 400
    if not request.headers.get("HX-Request") == "true":
        return HttpResponseBadRequest(
            "This endpoint is for HTMX requests only."
        )
    fixture_filter = FixtureFilter(request.GET or None)
    return render(
        request,
        "league/partials/fixtures_filter_panel_inner.html",
        {"filter": fixture_filter},
    )
