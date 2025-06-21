from datetime import timedelta
from django.http import HttpResponseBadRequest
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import (
    Week,
    Fixture,
    SinglesMatch,
    DoublesMatch,
    Season,
    FixtureResult,
    Team,
)
from .filters import FixtureFilter


# Helper functions
def get_default_team_data(team):
    """
    Defines the default team data for use in the generate_league_tables
    helper function.
    """

    return {
        "name": team.team_name,
        "P": 0,
        "W": 0,
        "D": 0,
        "L": 0,
        "team_sets_won": 0,
        "individual_sets_won": 0,
        "Pts": 0,
    }


def generate_league_table(season, division):
    """
    Generates the league table data for a given season and division.

    Calculates points from team wins, draws and losses.

    Teams are sorted in the final table by:
    1. Total points (Pts) - 2 for a win, 1 for a draw
    2. Number of wins (W)
    3. Team sets won (team_sets_won)
    4. Individual sets won (individual_sets_won)

    Args:
        season (Season): The season for which to generate the league table.
        division (Division): The division within the season.

    Returns:
        list[dict]: A list of dictionaries, each containing the team stats
                    and sorted in league table order.
    """

    POINTS_FOR_WIN = 2
    POINTS_FOR_DRAW = 1

    # Prefetch all teams for the division in the given season
    teams = Team.objects.filter(season=season, division=division)

    # Initialize all teams with default data
    teams_data = {team: get_default_team_data(team) for team in teams}

    # Query all fixture results for the season/division
    fixture_results_qs = FixtureResult.objects.filter(
        fixture__season=season, fixture__division=division
    ).select_related("fixture", "fixture__home_team", "fixture__away_team")

    for result in fixture_results_qs:
        home_team = result.fixture.home_team
        away_team = result.fixture.away_team

        # Update matches played
        teams_data[home_team]["P"] += 1
        teams_data[away_team]["P"] += 1

        # Update Team Sets
        teams_data[home_team]["team_sets_won"] += result.home_score
        teams_data[away_team]["team_sets_won"] += result.away_score

        # Win/draw/loss
        if result.winner == "home":
            teams_data[home_team]["W"] += 1
            teams_data[away_team]["L"] += 1
            teams_data[home_team]["Pts"] += POINTS_FOR_WIN
        elif result.winner == "away":
            teams_data[away_team]["W"] += 1
            teams_data[home_team]["L"] += 1
            teams_data[away_team]["Pts"] += POINTS_FOR_WIN
        elif result.winner == "draw":
            teams_data[home_team]["D"] += 1
            teams_data[away_team]["D"] += 1
            teams_data[home_team]["Pts"] += POINTS_FOR_DRAW
            teams_data[away_team]["Pts"] += POINTS_FOR_DRAW

        # --- Singles Matches Won ---
        for sm in result.singles_matches.all():
            teams_data[home_team]["individual_sets_won"] += sm.home_sets
            teams_data[away_team]["individual_sets_won"] += sm.away_sets

        # --- Track doubles match win ---
        if hasattr(result, "doubles_match"):
            dm = result.doubles_match
            teams_data[home_team]["individual_sets_won"] += dm.home_sets
            teams_data[away_team]["individual_sets_won"] += dm.away_sets

    # Sort by points, then team wins then singles/doubles match wins
    sorted_result = sorted(
        teams_data.values(),
        key=lambda x: (
            -x["Pts"],
            -x["W"],
            -x["team_sets_won"],
            -x["individual_sets_won"],
        ),
    )
    return sorted_result


# Views for pages
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
            away_player_win_counts[player] += 1

    # Get doubles winning team
    doubles_winning_team = None
    doubles_match = getattr(fixture.result, "doubles_match", None)
    if doubles_match:
        doubles_winning_team = doubles_match.winner

    return render(
        request,
        "league/result_breakdown.html",
        {
            "fixture": fixture,
            "home_player_win_counts": home_player_win_counts,
            "away_player_win_counts": away_player_win_counts,
            "doubles_winning_team": doubles_winning_team,
        },
    )


def tables(request):

    division_tables = []
    season = Season.objects.filter(is_current=True).first()

    if season:
        divisions = season.divisions.all()

        division_tables = [
            {
                "division": division,
                "table": generate_league_table(season, division),
            }
            for division in divisions
        ]

    # Build context
    context = {
        "season": season,
        "division_tables": division_tables,
    }

    return render(request, "league/tables.html", context)


# View for filter panel
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
