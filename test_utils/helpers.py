import calendar
from datetime import date, datetime, timedelta, time
from django.utils import timezone
from django.core.exceptions import ValidationError
from league.models import (
    Division,
    Season,
    Week,
    Team,
    Fixture,
    FixtureResult,
    SinglesMatch,
    Player,
    TeamPlayer,
    DoublesMatch,
    SinglesGame,
    DoublesGame,
)
from clubs.models import Club, Venue, VenueInfo, ClubReview


# --- Helpers for field validation ---
def helper_test_boolean_default(field_name, default_value, model, info_data):
    """
    Test that a boolean field has the correct default value.

    Args:
        field_name (str): The name of the boolean field to test.
        default_value (bool): The expected default value of the field.
        model (Model): The Django model class to test.
        info_data (dict): Dictionary of valid model data for required fields.

    Returns:
        bool: True if the field's value matches the default; False otherwise.
    """
    # Amend info_data
    info_data.pop(field_name, None)

    # Create test_object from info_data
    test_object = model.objects.create(**info_data)

    # Check placeholder is recorded as default
    result = getattr(test_object, field_name) == default_value

    # Return result
    return result


def helper_test_required_fields(
    test_case, test_object, field_name, is_required
):
    """
    Assert that a field is correctly assigned as required or optional.

    Args:
        test_case (TestCase): The test case instance calling this helper.
        test_object (Model): The Django model instance to validate.
        field_name (str): The name of the field being tested.
        is_required (bool): Indicates whether field should be required or not

    Raises:
        AssertionError: If field's validation does not match expectations.
    """
    with test_case.assertRaises(ValidationError) as cm:
        test_object.full_clean()
    errors = cm.exception.message_dict

    model_name = test_object.__class__.__name__

    if is_required:
        test_case.assertIn(
            field_name,
            errors,
            msg=f"{field_name} should be required in {model_name}",
        )
    else:
        test_case.assertNotIn(
            field_name,
            errors,
            msg=f"{field_name} should not be required in {model_name}",
        )


def helper_test_max_length(
    test_case, model, info_data, field_name, max_length
):
    """
    Validate that a field enforces its maximum length constraint.

    Args:
        test_case (TestCase): The test case instance calling this helper.
        model (Model): The Django model class to test.
        info_data (dict): Dictionary of valid model data.
        field_name (str): The name of the field being tested.
        max_length (int): The maximum allowed length of the field.

    Raises:
        ValidationError: If the field value exceeds the defined max_length.
    """
    # Create object
    test_object = model(**info_data)

    # Check valid at threshold
    setattr(test_object, field_name, "a" * max_length)
    test_object.full_clean()

    # Check invalid above threshold
    setattr(test_object, field_name, "a" * (max_length + 1))
    with test_case.assertRaises(ValidationError):
        test_object.full_clean()


# --- Helpers for debugging tests ---
def debug_response_as_file(response, file_path="debug_response.html"):
    """
    Write the response content bytes or string to a normal HTML file
    and automatically open browser for viewing.

    Args:
        response_content (bytes or str): The content to write.
        file_path (str): The path where the file will be written.

    Usage:
        debug_response_as_file(response)  # Creates file in project root dir

    Returns:
        str: The path to the file written.
    """

    # Import webbrowser inside function since only used when debugging
    # and reduces overhead when not in use
    import webbrowser

    # Decode bytes to string if needed
    if isinstance(response.content, bytes):
        content_str = response.content.decode("utf-8")
    else:
        content_str = response.content

    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content_str)

    # Open in browser for inspection
    webbrowser.open(f"{file_path}")

    return file_path


# --- Helpers for test setup ---
def create_fixture_result_setup():
    club = create_club("Test Club")
    division = create_division(name="Division 1", rank=1)
    season = create_season(
        name="2024/25",
        short_name="24-25",
        slug="24-25",
        start_year=2024,
        end_year=2025,
        is_current=True,
        divisions_list=[division],
    )
    venue = create_venue("Venue 1")

    team1 = create_team(
        season=season,
        division=division,
        club=club,
        venue=venue,
        team_name="Team A",
        home_day="monday",
        home_time=time(19, 0),
    )
    team2 = create_team(
        season=season,
        division=division,
        club=club,
        venue=venue,
        team_name="Team B",
        home_day="tuesday",
        home_time=time(19, 0),
    )

    week = create_week(season=season, week_num=1)

    fixture = create_fixture(
        season=season,
        division=division,
        week=week,
        home_team=team1,
        away_team=team2,
    )

    fixture_result = create_fixture_result(
        fixture=fixture,
        home_score=7,
        away_score=3,
    )

    return {
        "club": club,
        "division": division,
        "season": season,
        "venue": venue,
        "team1": team1,
        "team2": team2,
        "week": week,
        "fixture": fixture,
        "fixture_result": fixture_result,
    }


# --- Helpers for object creation and deletion ---
# Clubs app
def create_club(name):
    return Club.objects.create(name=name)


def create_club_review(
    club, user, score, headline, review_text, approved=True
):
    return ClubReview.objects.create(
        club=club,
        user=user,
        score=score,
        headline=headline,
        review_text=review_text,
        approved=approved,
    )


def create_venue(name):
    return Venue.objects.create(name=name)


def create_venue_info(
    venue,
    street_address="1 Main Street",
    address_line_2="",
    city="York",
    county="Yorkshire",
    postcode="YO19 5NG",
    num_tables=2,
    parking_info="Car park at the front of the venue",
    meets_league_standards=True,
    created_on=datetime.now(),
    approved=True,
    latitude=53.96423,
    longitude=-0.97813,
):
    venue_info = VenueInfo.objects.create(
        venue=venue,
        street_address=street_address,
        address_line_2=address_line_2,
        city=city,
        county=county,
        postcode=postcode,
        num_tables=num_tables,
        parking_info=parking_info,
        meets_league_standards=meets_league_standards,
        created_on=created_on,
        approved=approved,
        latitude=latitude,
        longitude=longitude,
    )
    return venue_info


# League app
def create_division(name, rank):
    return Division.objects.create(name=name, rank=rank)


def create_doubles_game(doubles_match, set_num, home_points, away_points):
    return DoublesGame.objects.create(
        doubles_match=doubles_match,
        set_num=set_num,
        home_points=home_points,
        away_points=away_points
    )


def create_doubles_match(
    fixture_result, home_players, away_players, home_sets, away_sets
):
    match = DoublesMatch.objects.create(
        fixture_result=fixture_result,
        home_sets=home_sets,
        away_sets=away_sets,
    )
    match.home_players.set(home_players)
    match.away_players.set(away_players)
    return match


def create_fixture(season, division, week, home_team, away_team):
    # Get weekday integer (0=Monday)
    home_weekday = list(calendar.day_name).index(
        home_team.home_day.capitalize()
    )

    # Get fixture date for start of week
    fixture_date = week.start_date

    # Offset fixture date by weekday integer
    fixture_date += timedelta(
        days=(home_weekday - week.start_date.weekday()) % 7
    )

    # Get fixture datetime
    fixture_datetime = timezone.make_aware(
        datetime(
            fixture_date.year,
            fixture_date.month,
            fixture_date.day,
            home_team.home_time.hour,
            home_team.home_time.minute,
        )
    )

    return Fixture.objects.create(
        season=season,
        division=division,
        week=week,
        datetime=fixture_datetime,
        home_team=home_team,
        away_team=away_team,
        venue=home_team.home_venue,
        status="scheduled",
    )


def create_fixture_result(
    fixture, home_score, away_score, winner=None, status="played"
):
    return FixtureResult.objects.create(
        fixture=fixture,
        home_score=home_score,
        away_score=away_score,
        winner=winner,
        status=status,
    )


def create_player(
    forename,
    surname,
    current_club,
    date_of_birth=date(2000, 1, 1),
    club_status="confirmed",
):

    return Player.objects.create(
        forename=forename,
        surname=surname,
        date_of_birth=date_of_birth,
        current_club=current_club,
        club_status=club_status,
    )


def create_season(
    name, short_name, slug, start_year, end_year, is_current, divisions_list
):
    season = Season.objects.create(
        name=name,
        short_name=short_name,
        slug=slug,
        start_date=date(start_year, 9, 1),
        end_date=date(end_year, 5, 1),
        registration_opens=timezone.make_aware(datetime(start_year, 6, 1)),
        registration_closes=timezone.make_aware(datetime(start_year, 8, 1)),
        is_visible=True,
        is_current=is_current,
    )
    season.divisions.set(divisions_list)
    return season


def create_singles_match(
    fixture_result, home_player, away_player, home_sets, away_sets
):
    return SinglesMatch.objects.create(
        fixture_result=fixture_result,
        home_player=home_player,
        away_player=away_player,
        home_sets=home_sets,
        away_sets=away_sets,
    )


def create_singles_game(singles_match, set_num, home_points, away_points):
    return SinglesGame.objects.create(
        singles_match=singles_match,
        set_num=set_num,
        home_points=home_points,
        away_points=away_points
    )


def create_team(season, division, club, venue, team_name, home_day, home_time):
    return Team.objects.create(
        season=season,
        division=division,
        club=club,
        home_venue=venue,
        team_name=team_name,
        home_day=home_day,
        home_time=home_time,
        approved=True,
    )


def create_team_player(player, team, paid_fees=True):
    return TeamPlayer.objects.create(
        player=player,
        team=team,
        paid_fees=paid_fees,
    )


def create_week(season, week_num):
    return Week.objects.create(
        season=season,
        name=f"Week {week_num} {season.short_name}",
        details="",
        start_date=season.start_date + timedelta(weeks=week_num - 1),
    )


def delete_club_reviews(**filters):
    """
    Helper to delete objects from ClubReview model with optional filters.

    Args:
        **filters: Optional keyword arguments for filtering.
    """
    delete_objects(ClubReview, **filters)


def delete_fixtures(**filters):
    """
    Helper to delete objects from Fixture model with optional filters.

    Args:
        **filters: Optional keyword arguments for filtering.
    """
    delete_objects(Fixture, **filters)


def delete_objects(model, **filters):
    """
    Generic helper to delete objects from a Django model with optional filters.

    Args:
        model (Model): The Django model class (e.g., Fixture).
        **filters: Optional keyword arguments for filtering.

    Usage:
        delete_objects(Fixture)  # Deletes all Fixture instances
        delete_objects(Fixture, season=season_1)  # Deletes filtered Fixtures
    """
    model.objects.filter(**filters).delete()


def delete_weeks(**filters):
    """
    Helper to delete objects from Week model with optional filters.

    Args:
        **filters: Optional keyword arguments for filtering.
    """
    delete_objects(Week, **filters)
