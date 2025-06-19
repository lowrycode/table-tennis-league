from datetime import timedelta
from django.http import HttpResponseBadRequest
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Week, Fixture, SinglesMatch, DoublesMatch
from .filters import FixtureFilter


def fixtures(request):
    """
    Displays the fixture list, filtered by season and optionally division
    and club.

    Supports both full-page rendering and partial updates via HTMX.
    Filters are applied using FixtureFilter, and results are grouped by weeks.
    """

    # Prefetch related data for efficiency
    all_fixtures = Fixture.objects.select_related(
        "season", "division", "home_team__club", "away_team__club"
    )

    # Apply filters from GET params using FixtureFilter
    fixture_filter = FixtureFilter(request.GET, queryset=all_fixtures)
    filtered_fixtures_qs = fixture_filter.qs

    # Get season from bound form - defaults to current season or None
    if fixture_filter.is_valid():
        season = fixture_filter.form.cleaned_data.get("season")
    else:
        season = None

    # Get season_weeks
    current_week_id = None
    if season:
        season_weeks = (
            Week.objects.filter(season=season)
            .prefetch_related(
                Prefetch("week_fixtures", queryset=filtered_fixtures_qs)
            )
            .order_by("start_date")
        )

        # Find current week (start_date <= today <= end_date)
        today = timezone.now().date()
        for week in season_weeks:
            if week.start_date <= today <= week.start_date + timedelta(days=6):
                current_week_id = week.id
                break
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
        "current_week_id": current_week_id,
    }

    # If htmx request, return only the fixtures_section partial template
    if request.headers.get("HX-Request") == "true":
        return render(
            request, "league/partials/fixtures_section.html", context
        )

    return render(request, "league/fixtures.html", context)


def results(request):
    """
    Displays the results list, filtered by season and optionally division
    and club.

    Supports both full-page rendering and partial updates via HTMX.
    Filters are applied using FixtureFilter and results are grouped by weeks.
    """

    # Prefetch related data for efficiency
    fixtures_with_results = Fixture.objects.select_related(
        "season", "division", "home_team__club", "away_team__club", "result"
    ).filter(result__isnull=False)

    # Apply filters from GET params using FixtureFilter
    fixture_filter = FixtureFilter(request.GET, queryset=fixtures_with_results)
    filtered_fixtures_qs = fixture_filter.qs

    # Get season from bound form - defaults to current season or None
    if fixture_filter.is_valid():
        season = fixture_filter.form.cleaned_data.get("season")
    else:
        season = None

    # Get season_weeks
    if season:
        season_weeks = (
            Week.objects.filter(
                season=season, week_fixtures__in=filtered_fixtures_qs
            )
            .prefetch_related(
                Prefetch("week_fixtures", queryset=filtered_fixtures_qs)
            )
            .distinct()
            .order_by("-start_date")
        )

    else:
        season_weeks = None

    # Deduce whether filters are applied by checking for get parameters
    filters_applied = len(request.GET) > 0

    # Build context
    context = {
        "season": season,
        "weeks": season_weeks,
        "filter": fixture_filter,
        "filters_applied": filters_applied,
    }

    # If htmx request, return only the results_section partial template
    if request.headers.get("HX-Request") == "true":
        return render(request, "league/partials/results_section.html", context)

    return render(request, "league/results.html", context)


def result_breakdown(request, fixture_id):
    """
    Display a detailed breakdown of a fixture's result, including singles
    and doubles match scores and individual player win counts.

    If no result exists for the given fixture, the user is redirected to
    the results page with a warning.

    Args:
        request (HttpRequest): The HTTP request object.
        fixture_id (int): The ID of the fixture with the related results.

    Returns:
        HttpResponse: Rendered result breakdown page or redirect to
        the results page.
    """
    # Define querysets
    singles_qs = SinglesMatch.objects.select_related(
        "home_player__player", "away_player__player"
    ).prefetch_related("singles_games")

    doubles_qs = DoublesMatch.objects.prefetch_related(
        "home_players__player", "away_players__player", "doubles_games"
    )

    fixture_qs = Fixture.objects.select_related("result").prefetch_related(
        Prefetch("result__singles_matches", queryset=singles_qs),
        Prefetch("result__doubles_match", queryset=doubles_qs),
    )

    # Get fixture with prefetched data
    fixture = get_object_or_404(fixture_qs, id=fixture_id)

    # Redirect to Results page if fixture has no result
    if not hasattr(fixture, "result"):
        messages.warning(request, "No result found for this fixture.")
        return redirect("results")

    # Count singles wins for both home and away players
    home_player_win_counts = {}
    away_player_win_counts = {}
    for match in fixture.result.singles_matches.all():
        if match.winner == "home":
            player = match.home_player.player
            if player not in home_player_win_counts:
                home_player_win_counts[player] = 0
            home_player_win_counts[player] += 1
        elif match.winner == "away":
            player = match.away_player.player
            if player not in away_player_win_counts:
                away_player_win_counts[player] = 0
            away_player_win_counts[player] = 1

    return render(
        request, "league/result_breakdown.html", {
            "fixture": fixture,
            "home_player_win_counts": home_player_win_counts,
            "away_player_win_counts": away_player_win_counts,
        },
    )


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
