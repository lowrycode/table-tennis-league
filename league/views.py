from datetime import timedelta
from django.http import HttpResponseBadRequest
from django.db.models import Prefetch, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import (
    Week,
    Fixture,
    SinglesMatch,
    DoublesMatch,
    FixtureResult,
    Team,
    Season,
    TeamPlayer,
)
from .filters import FixtureFilter
from .forms import LeagueTableForm


# Constants
POINTS_FOR_WIN = 2
POINTS_FOR_DRAW = 1


# Helper functions
def get_default_team_data(team):
    """
    Defines the default team data for use in the generate_league_tables
    helper function.

    Args:
        team (Team): The team instance for which default data is generated.

    Returns:
        dict: A dictionary containing default team data with keys:
            - 'id' (int): The team's unique identifier.
            - 'name' (str): The team's name.
            - 'P' (int): Matches played (default as 0).
            - 'W' (int): Matches won (default as 0).
            - 'D' (int): Matches drawn (default as 0).
            - 'L' (int): Matches lost (default as 0).
            - 'team_sets_won' (int): Number of team sets won (default as 0).
            - 'individual_sets_won' (int): Number of individual sets won
                                           (default as 0).
            - 'Pts' (int): Points earned (default as 0).
    """

    return {
        "id": team.id,
        "name": team.team_name,
        "P": 0,
        "W": 0,
        "D": 0,
        "L": 0,
        "team_sets_won": 0,
        "individual_sets_won": 0,
        "Pts": 0,
    }


def get_fixture_data(team, fixture):
    """
    Builds a dictionary of summary information for an unplayed fixture
    for the specified team.

    Args:
        team (Team): The team for which the fixture is being viewed.
        fixture (Fixture): The fixture object containing match details.

    Returns:
        dict: A dictionary containing:
            - 'week' (Week): The week object associated with the fixture.
            - 'datetime' (datetime): Scheduled date and time of the fixture.
            - 'home_team' (Team): The team playing at home.
            - 'away_team' (Team): The team playing away.
            - 'opponent' (Team): The opposing team from perspective of `team`.
            - 'home_or_away' (str): From perspective of 'team'.
            - 'venue' (Venue): The venue object for the fixture.
    """

    # Get fixture week and date
    week = fixture.week
    datetime = fixture.datetime

    # Get opponent and venue
    if fixture.home_team == team:
        opponent = fixture.away_team
        home_or_away = "Home"
    else:
        opponent = fixture.home_team
        home_or_away = "Away"

    return {
        "week": week,
        "datetime": datetime,
        "home_team": fixture.home_team,
        "away_team": fixture.away_team,
        "opponent": opponent,
        "home_or_away": home_or_away,
        "venue": fixture.venue,
    }


def get_player_match_stats(team_player, team, registered_player_ids):
    """
    Calculates match statistics for a given player when playing for the
    specified team.

    Determines whether the player is officially registered with the team or
    is a reserve. Considers only singles match records for fixtures where
    they represented the specified team.

    Args:
        team_player (TeamPlayer): The player to calculate stats for.
        team (Team): The team for which the stats are calculated.
        registered_player_ids (set[int]): A set of IDs for players registered
                                          to the team.

    Returns:
        dict: A dictionary containing:
            - 'name' (str): Full name of the player.
            - 'is_registered' (bool): Whether the player is officially
                                      registered to the team.
            - 'played' (int): Total number of singles matches played for the
                              specified team.
            - 'wins' (int): Number of singles matches won.
            - 'percent' (float): Win percentage (rounded to 1 decimal place).
    """
    # Deduce whether player is registered for the team (or a reserve)
    is_registered = team_player.id in registered_player_ids

    # Get matches where team player or reserve is playing for this team
    matches = SinglesMatch.objects.filter(
        Q(home_player=team_player, fixture_result__fixture__home_team=team)
        | Q(away_player=team_player, fixture_result__fixture__away_team=team)
    )

    # Count matches played
    played = matches.count()

    # Count wins
    wins = matches.filter(
        (Q(home_player=team_player) & Q(winner="home"))
        | (Q(away_player=team_player) & Q(winner="away"))
    ).count()

    # Count percentage wins
    percent = round((wins / played) * 100, 1) if played else 0.0

    return {
        "name": f"{team_player.player.full_name}",
        "is_registered": is_registered,
        "played": played,
        "wins": wins,
        "percent": percent,
    }


def get_result_data(team, fixture, fixture_result):
    """
    Builds a summary dictionary for a fixture result.

    Args:
        team (Team): The team for which the summary is being generated.
        fixture (Fixture): The fixture object representing the match.
        fixture_result (FixtureResult): The result of the fixture.

    Returns:
        dict: A dictionary containing:
            - 'week' (Week): The week object associated with the fixture.
            - 'home_team' (Team): The team playing at home.
            - 'away_team' (Team): The team playing away.
            - 'opponent' (Team): The opposing team from perspective of `team`.
            - 'home_or_away' (str): From perspective of 'team'.
            - 'venue' (Venue): The venue object for the fixture.
            - 'outcome' (str): "Win", "Lose", or "Draw".
            - 'result' (FixtureResult): The full result object

    """

    week = fixture.week

    # Get opponent and home_or_away
    if fixture.home_team == team:
        opponent = fixture.away_team
        home_or_away = "Home"
    else:
        opponent = fixture.home_team
        home_or_away = "Away"

    # Get match outcome (Win, Lose, Draw)
    if fixture_result.winner.lower() == "draw":
        outcome = "Draw"
    elif fixture_result.winner.lower() == home_or_away.lower():
        outcome = "Win"
    else:
        outcome = "Lose"

    return {
        "week": week,
        "home_team": fixture.home_team,
        "away_team": fixture.away_team,
        "opponent": opponent,
        "home_or_away": home_or_away,
        "venue": fixture.venue,
        "outcome": outcome,
        "result": fixture_result,
    }


def get_team_summary_stats(results_data):
    """
    Calculates summary statistics for a team's performance.

    Args:
        results_data (list[dict]): A list of dictionaries representing fixture
                                   results. Each dictionary should contain
                                   an 'outcome' key with one of the values:
                                   "Win", "Draw", or "Lose".

    Returns:
        dict: A dictionary containing the summary statistics:
            - 'played' (int): Total number of matches played.
            - 'wins' (int): Number of matches won.
            - 'draws' (int): Number of matches drawn.
            - 'losses' (int): Number of matches lost.
            - 'points' (int): Total points earned.
    """
    played = len(results_data)
    wins = 0
    draws = 0
    losses = 0
    points = 0
    for result in results_data:
        if result["outcome"].lower() == "win":
            wins += 1
            points += POINTS_FOR_WIN
        elif result["outcome"].lower() == "draw":
            draws += 1
            points += POINTS_FOR_DRAW
        elif result["outcome"].lower() == "lose":
            losses += 1

    return {
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "points": points,
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

    # Get all teams for the specified season and division
    teams = Team.objects.filter(season=season, division=division)

    # Initialize all teams with default data
    teams_data = {team: get_default_team_data(team) for team in teams}

    # Prefetch fixture result queryset
    fixture_results_qs = (
        FixtureResult.objects.filter(
            fixture__season=season, fixture__division=division
        )
        .select_related("fixture", "fixture__home_team", "fixture__away_team")
        .prefetch_related("singles_matches", "doubles_match")
    )

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

        # Singles Matches Won
        for sm in result.singles_matches.all():
            teams_data[home_team]["individual_sets_won"] += sm.home_sets
            teams_data[away_team]["individual_sets_won"] += sm.away_sets

        # Track doubles match win
        if hasattr(result, "doubles_match"):
            dm = result.doubles_match
            teams_data[home_team]["individual_sets_won"] += dm.home_sets
            teams_data[away_team]["individual_sets_won"] += dm.away_sets

    # Sort by points, then team match wins then team sets,
    # then singles/doubles match sets
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
    """
    Displays the league tables page with optional season filtering
    (defaults to current season).

    Supports HTMX for filtering.
    """
    form = LeagueTableForm(request.GET or None)

    if form.is_valid():
        season = form.cleaned_data["season"]
    else:
        season = Season.objects.filter(is_current=True).first()

    if season:
        season_divisions = season.divisions.all()
        division_tables = [
            {
                "division": division,
                "table": generate_league_table(season, division),
            }
            for division in season_divisions
        ]
    else:
        division_tables = []

    # Deduce whether filters are applied by checking for get parameters
    filters_applied = len(request.GET) > 0

    # Build context
    context = {
        "season": season,
        "division_tables": division_tables,
        "form": form,
        "filters_applied": filters_applied,
    }

    # If htmx request, return only the tables_section partial template
    if request.headers.get("HX-Request") == "true":
        return render(request, "league/partials/tables_section.html", context)

    return render(request, "league/tables.html", context)


def team_summary(request, team_id):
    """
    Displays the summary page for a specific team including
    - team summary details and stats
    - performance stats for each team player (including reserves)
    - fixture results
    - upcoming fixtures

    Args:
        request (HttpRequest): The incoming HTTP request.
        team_id (int): The primary key of the team to summarize.

    Returns:
        HttpResponse: Rendered HTML page displaying the team summary
                      or 404 page.
    """

    team = get_object_or_404(Team, id=team_id)

    team_fixtures_qs = (
        Fixture.objects.filter(Q(home_team=team) | Q(away_team=team))
        .select_related("result", "venue", "home_team", "away_team")
        .prefetch_related("result__singles_matches", "result__doubles_match")
    )

    # Get registered players and IDs for quick lookup
    registered_players = TeamPlayer.objects.filter(team=team)
    registered_player_ids = set(
        registered_players.values_list("id", flat=True)
    )

    # Get players who played singles matches for the team
    singles_players = TeamPlayer.objects.filter(
        Q(home_singles_matches__fixture_result__fixture__home_team=team)
        | Q(away_singles_matches__fixture_result__fixture__away_team=team)
    )

    # Combine all team players (registered + played)
    all_team_players = registered_players | singles_players
    all_team_players = all_team_players.distinct().select_related("player")

    # Get player summary data
    player_data = []
    for team_player in all_team_players:
        data = get_player_match_stats(team_player, team, registered_player_ids)
        player_data.append(data)

    # Sort player summary data by percentage wins
    player_data = sorted(
        player_data, key=lambda x: (x["percent"], x["wins"]), reverse=True
    )

    # Get fixtures and results
    fixture_data = []
    results_data = []
    for fixture in team_fixtures_qs:
        fixture_result = getattr(fixture, "result", None)
        if fixture_result:
            data = get_result_data(team, fixture, fixture_result)
            results_data.append(data)
        else:
            data = get_fixture_data(team, fixture)
            fixture_data.append(data)

    # Get Team Stats
    team_stats = get_team_summary_stats(results_data)

    # Build context
    context = {
        "team": team,
        "player_data": player_data,
        "fixtures_data": fixture_data,
        "results_data": results_data,
        "team_stats": team_stats,
    }

    return render(request, "league/team_summary.html", context)


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
