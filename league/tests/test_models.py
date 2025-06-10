from datetime import date, datetime, time
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from test_utils.helpers import (
    helper_test_required_fields,
    helper_test_max_length,
)
from league.models import (
    Division,
    Season,
    Week,
    Player,
    TeamPlayer,
    Team,
    Fixture,
)
from clubs.models import Club, Venue


class DivisionTests(TestCase):
    """
    Unit tests for the Division model to verify field behaviour, validation,
    string representation and ordering.
    """

    def test_can_create_division(self):
        """Verify division can be saved and retrieved correctly."""
        division = Division.objects.create(name="Division 1", rank=1)
        self.assertTrue(Division.objects.filter(id=division.id).exists())

    def test_string_representation(self):
        """Verify string representation returns the division name."""
        division = Division.objects.create(name="Division 1", rank=1)
        self.assertEqual(str(division), division.name)

    def test_divisions_are_ordered_by_rank(self):
        """Verify divisions are ordered from lowest to highest rank number"""
        Division.objects.create(name="A", rank=2)
        Division.objects.create(name="B", rank=1)
        Division.objects.create(name="C", rank=3)

        divisions = list(Division.objects.all())
        ranks = [d.rank for d in divisions]

        self.assertEqual(ranks, sorted(ranks))  # should be [1, 2, 3]

    # Multi-field tests
    def test_required_fields(self):
        """
        Verify that both fields are required using helper function.
        """
        required_fields = {
            "name": True,
            "rank": True,
        }

        test_object = Division()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """
        Verify fields with max length constraints are properly enforced
        using helper function.
        """
        fields = {
            "name": 50,
        }

        # Check each field
        valid_data = {"name": "Division 1", "rank": 1}
        test_model = Division
        for field, max_length in fields.items():
            helper_test_max_length(
                self, test_model, valid_data, field, max_length
            )

    # Field constraints
    def test_name_must_be_unique(self):
        """Verify division name must be unique."""
        Division.objects.create(name="Division 1", rank=1)
        with self.assertRaises(IntegrityError):
            Division.objects.create(name="Division 1", rank=2)

    def test_rank_must_be_unique(self):
        """Verify division rank must be unique."""
        Division.objects.create(name="Division 1 North", rank=1)
        with self.assertRaises(IntegrityError):
            Division.objects.create(name="Division 1 South", rank=1)

    def test_cannot_delete_if_linked_to_season(self):
        """Verify division cannot be deleted if used in a season."""
        division = Division.objects.create(name="Division 1", rank=1)

        # Create season which links to this division
        season_data = {
            "name": "2024-25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }
        season = Season.objects.create(**season_data)
        season.divisions.set([division])
        with self.assertRaisesMessage(
            ValidationError,
            (
                "This division cannot be deleted because it is linked "
                "to season data."
            ),
        ):
            division.delete()


class SeasonTests(TestCase):
    """
    Unit tests for the Season model to verify field behaviour, validation,
    string representation and ordering.
    """

    def setUp(self):
        """
        Create divisions, seasons and related data ready for tests.
        """
        self.division_1 = Division.objects.create(name="Division 1", rank=1)
        self.division_2 = Division.objects.create(name="Division 2", rank=2)
        self.data = {
            "name": "2024-25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }
        self.season = Season.objects.create(**self.data)
        self.season.divisions.set([self.division_1, self.division_2])

        self.unsaved_data = {
            "name": "not-in-database",
            "short_name": "not-in-database",
            "slug": "not-in-database",
            "start_date": date(2023, 9, 1),
            "end_date": date(2024, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": False,
        }

    def test_can_create_season(self):
        """Verify setup data is valid and season object is created."""
        self.season.full_clean()
        self.season.save()
        self.assertTrue(Season.objects.filter(id=self.season.id).exists())

    def test_string_representation(self):
        """Verify string representation returns the season name."""
        self.assertEqual(str(self.season), self.season.name)

    # Multi-field tests
    def test_required_fields(self):
        """
        Verify 'required status' for each field using helper function.
        """
        required_fields = {
            "name": True,
            "short_name": True,
            "slug": True,
            "start_date": True,
            "end_date": True,
            "registration_opens": True,
            "registration_closes": True,
            "is_visible": False,
            "is_current": False,
        }

        test_object = Season()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """
        Verify fields with max length constraints are properly enforced
        using helper function.
        """
        fields = {
            "name": 100,
            "short_name": 20,
            "slug": 20,
        }

        # Check each field
        valid_data = self.unsaved_data.copy()
        test_model = Season
        for field, max_length in fields.items():
            helper_test_max_length(
                self, test_model, valid_data, field, max_length
            )

    # Field constraints
    def test_name_must_be_unique(self):
        """Verify season name must be unique."""
        data = self.unsaved_data.copy()
        data["name"] = self.data["name"]

        with self.assertRaises(IntegrityError):
            Season.objects.create(**data)

    def test_short_name_must_be_unique(self):
        """Verify season short name must be unique."""
        data = self.unsaved_data.copy()
        data["short_name"] = self.data["short_name"]

        with self.assertRaises(IntegrityError):
            Season.objects.create(**data)

    def test_slug_must_be_unique(self):
        """Verify season slug must be unique."""
        data = self.unsaved_data.copy()
        data["slug"] = self.data["slug"]

        with self.assertRaises(IntegrityError):
            Season.objects.create(**data)

    def test_at_least_one_division_is_required(self):
        """Verify at least one division must be chosen for a season."""
        self.season.divisions.set([])
        with self.assertRaises(ValidationError):
            self.season.full_clean()

    def test_start_date_must_be_earlier_than_end_date(self):
        """
        Verify start_date before end_date is valid and end_date before
        start_date is invalid.
        """
        now = timezone.now().date()

        # Should pass since start date is before end date
        self.season.start_date = now - timezone.timedelta(days=1)
        self.season.end_date = now + timezone.timedelta(days=1)
        self.season.full_clean()

        # Should fail since start date is after end date
        self.season.start_date = now + timezone.timedelta(days=5)
        with self.assertRaises(ValidationError):
            self.season.full_clean()

    def test_registration_opens_must_be_earlier_than_registration_closes(self):
        """
        Verify registration_opens before registration_closes is valid and
        registration_closes before registration_opens is invalid.
        """
        now = timezone.now()

        # Should pass since registration_opens is before registration_closes
        self.season.registration_opens = now - timezone.timedelta(days=30)
        self.season.registration_closes = now - timezone.timedelta(days=20)
        self.season.start_date = now.date() - timezone.timedelta(days=10)
        self.season.end_date = now.date() + timezone.timedelta(days=10)
        self.season.full_clean()

        # Should fail since registration_opens is after registration_closes
        self.season.registration_closes = now - timezone.timedelta(days=40)
        with self.assertRaises(ValidationError):
            self.season.full_clean()

    def test_registration_closes_must_be_earlier_than_start_date(self):
        """
        Verify registration_closes before start_date is valid and
        registration_closes after start_date is invalid.
        """
        now = timezone.now()

        # Should pass since registration_closes is before start date
        self.season.registration_opens = now - timezone.timedelta(days=30)
        self.season.registration_closes = now - timezone.timedelta(days=20)
        self.season.start_date = now.date() - timezone.timedelta(days=10)
        self.season.end_date = now.date() + timezone.timedelta(days=50)
        self.season.full_clean()

        # Should fail since registration_closes is after start date
        self.season.registration_closes = now + timezone.timedelta(days=10)
        with self.assertRaises(ValidationError):
            self.season.full_clean()

    def test_only_one_season_can_be_current(self):
        """
        Verify setting is_current=True unsets is_current on other seasons.
        """
        # Check is_current = True before adding new season
        self.assertTrue(self.season.is_current)

        # Create new season initially not current
        new_data = self.unsaved_data.copy()
        new_season = Season.objects.create(**new_data)
        self.assertFalse(new_season.is_current)
        self.assertTrue(self.season.is_current)

        # Set new_season as current and save
        new_season.is_current = True
        new_season.save()

        # Reload from DB
        self.season.refresh_from_db()
        new_season.refresh_from_db()

        # Assert only new season is current
        self.assertFalse(self.season.is_current)
        self.assertTrue(new_season.is_current)


class WeekTests(TestCase):
    """
    Unit tests for the Week model to verify field behaviour, validation,
    string representation and ordering.
    """

    def setUp(self):
        """Create Division, Season and Week objects ready for tests"""
        # Division needed for season
        self.division = Division.objects.create(name="Division 1", rank=1)
        self.data = {
            "name": "2024-25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }

        # Season needed for week
        self.season = Season.objects.create(**self.data)
        self.season.divisions.set([self.division])
        self.season.save()

        # Create week
        self.week_data = {
            "season": self.season,
            "name": "Week 1",
            "details": "",
            "start_date": date(2024, 9, 1),
        }
        self.week = Week.objects.create(**self.week_data)

    def test_can_create_week(self):
        """Verify week can be saved and retrieved correctly."""
        # Should pass without errors
        self.week.full_clean()
        self.week.save()
        self.assertTrue(Week.objects.filter(id=self.week.id).exists())

    def test_string_representation(self):
        """Verify string representation returns the week name."""
        self.assertEqual(str(self.week), self.week.name)

    def test_weeks_are_ordered_by_start_date_asc(self):
        """
        Verify weeks are ordered by start_date starting with earliest.
        """
        self.week.delete()
        now = timezone.now().date()

        week1_data = self.week_data.copy()
        week1_data["name"] = "A"
        week1_data["start_date"] = now + timezone.timedelta(weeks=1)
        week1 = Week.objects.create(**week1_data)

        week3_data = self.week_data.copy()
        week3_data["name"] = "B"
        week3_data["start_date"] = now + timezone.timedelta(weeks=3)
        week3 = Week.objects.create(**week3_data)

        week2_data = self.week_data.copy()
        week2_data["name"] = "C"
        week2_data["start_date"] = now + timezone.timedelta(weeks=2)
        week2 = Week.objects.create(**week2_data)

        weeks = list(Week.objects.all())
        self.assertEqual(weeks[0].name, week1.name)
        self.assertEqual(weeks[1].name, week2.name)
        self.assertEqual(weeks[2].name, week3.name)

    # Multi-field tests
    def test_required_fields(self):
        """
        Verify that both fields are required using helper function.
        """
        required_fields = {
            "season": True,
            "name": True,
            "details": False,
            "start_date": True,
        }

        test_object = Week()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """
        Verify fields with max length constraints are properly enforced
        using helper function.
        """
        fields = {
            "name": 50,
            "details": 100,
        }

        # Check each field
        self.week.delete()
        valid_data = self.week_data.copy()
        test_model = Week
        for field, max_length in fields.items():
            helper_test_max_length(
                self, test_model, valid_data, field, max_length
            )

    # Field constraints
    # def test_cannot_delete_if_linked_to_fixture(self):
    #     """Verify week cannot be deleted if linked to a fixture."""
    #     # Create fixture which links to this week
    #     fixture_data = {
    #         "something": "ADD THIS WHEN FIXTURE CREATED!!"
    #     }
    #     fixture = Fixture.objects.create(**fixture_data)
    #     with self.assertRaisesMessage(
    #         ValidationError,
    #         (
    #             "This week cannot be deleted because it is linked "
    #             "to league data."
    #         ),
    #     ):
    #         self.week.delete()


class PlayerTests(TestCase):
    """
    Unit tests for the Player model to verify field behaviour, validation,
    string representation, ordering, uniqueness, and deletion constraints.
    """

    def setUp(self):
        # Create a Club
        self.club = Club.objects.create(name="Test Club")

        # Base player data
        self.player_data = {
            "forename": "john",
            "surname": "doe",
            "date_of_birth": date(1990, 1, 1),
            "current_club": self.club,
            "club_status": "confirmed",
        }

        # Create Player
        self.player = Player.objects.create(**self.player_data)

    def test_can_create_player(self):
        """Verify player can be saved and retrieved correctly."""
        self.player.full_clean()
        self.player.save()
        self.assertTrue(Player.objects.filter(id=self.player.id).exists())

    def test_name_fields_are_title_cased_on_save(self):
        """Verify forename and surname are title cased on save."""
        self.assertEqual(self.player.forename, "John")
        self.assertEqual(self.player.surname, "Doe")

    def test_string_representation(self):
        """
        Verify string representation returns 'Surname, Forename' with
        title case.
        """
        self.assertEqual(str(self.player), "Doe, John (01 Jan 1990)")

    def test_full_name_property(self):
        """
        Verify full_name property returns 'Forename Surname' with title case.
        """
        self.assertEqual(self.player.full_name, "John Doe")

    def test_ordering_by_surname(self):
        """Verify players are ordered by surname ascending."""
        self.player.delete()
        Player.objects.create(
            forename="Alice", surname="Smith", date_of_birth=date(1991, 2, 2)
        )
        Player.objects.create(
            forename="Bob", surname="Anderson", date_of_birth=date(1989, 3, 3)
        )
        Player.objects.create(
            forename="Charlie", surname="Brown", date_of_birth=date(1992, 4, 4)
        )

        players = list(Player.objects.all())
        surnames = [p.surname for p in players]
        self.assertEqual(surnames, sorted(surnames))

    # Multi-field tests
    def test_required_fields(self):
        """Verify required fields: forename, surname, date_of_birth."""
        required_fields = {
            "forename": True,
            "surname": True,
            "date_of_birth": True,
        }

        test_object = Player()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """Verify max length for forename and surname fields."""
        fields = {
            "forename": 50,
            "surname": 50,
        }

        # Check each field
        valid_data = self.player_data.copy()
        test_model = Player
        for field, max_length in fields.items():
            helper_test_max_length(
                self, test_model, valid_data, field, max_length
            )

    # Single-field tests
    def test_club_status_choices_default(self):
        """Verify club_status defaults to 'pending' if not provided and only allows valid choices."""
        player = Player.objects.create(
            forename="Test",
            surname="Player",
            date_of_birth=date(2000, 1, 1),
            current_club=None,
        )
        self.assertEqual(player.club_status, "pending")

    def test_unique_forename_surname_date_of_birth(self):
        """Verify combination of forename, surname, and date_of_birth must be unique."""
        with self.assertRaises(IntegrityError):
            Player.objects.create(**self.player_data)

    def test_can_create_players_with_same_name_but_different_dob(self):
        """
        Verify players with same forename and surname but different DOB
        are allowed.
        """
        data = self.player_data.copy()
        data["date_of_birth"] = date(1991, 1, 1)
        player = Player.objects.create(**data)
        self.assertTrue(Player.objects.filter(id=player.id).exists())

    def test_cannot_delete_if_linked_to_player_seasons(self):
        """Verify player cannot be deleted if linked to player_seasons."""

        # Create division and season
        division = Division.objects.create(name="Division 1", rank=1)
        season_data = {
            "name": "2024/25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }
        season = Season.objects.create(**season_data)
        season.divisions.set([division])
        season.save()

        # Create venue and team
        venue = Venue.objects.create(name="Test Venue 1")
        team_data = {
            "season": season,
            "division": division,
            "club": self.club,
            "home_venue": venue,
            "team_name": "team awesome",
            "home_day": "monday",
            "home_time": time(19, 0),
            "approved": True,
        }
        team = Team.objects.create(**team_data)

        # Create TeamPlayer
        TeamPlayer.objects.create(
            player=self.player,
            team=team,
            paid_fees=True,
        )

        # Test deletion
        with self.assertRaises(ProtectedError):
            self.player.delete()

    def test_can_delete_player_if_not_linked(self):
        """Verify player can be deleted if not linked to any player_seasons."""
        self.player.delete()
        self.assertFalse(Player.objects.filter(id=self.player.id).exists())


class TeamPlayerTests(TestCase):
    """
    Unit tests for the TeamPlayer model to verify field behaviour,
    validation logic, string representation, ordering and uniqueness
    constraints.
    """

    def setUp(self):
        # Create clubs
        self.club1 = Club.objects.create(name="Test Club 1")
        self.club2 = Club.objects.create(name="Test Club 2")

        # Create a player
        self.player = Player.objects.create(
            forename="Jane",
            surname="Smith",
            date_of_birth=date(1990, 1, 1),
            current_club=self.club1,
            club_status="confirmed",
        )

        # Create division - needed for season and team
        self.division = Division.objects.create(name="Division 1", rank=1)

        # Season data
        self.season_data_1 = {
            "name": "2024/25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }

        # Create season - needed for team
        self.season1 = Season.objects.create(**self.season_data_1)
        self.season1.divisions.set([self.division])
        self.season1.save()

        # Create venue - needed for team
        self.venue = Venue.objects.create(name="Test Venue 1")

        # Create Team
        self.team_data = {
            "season": self.season1,
            "division": self.division,
            "club": self.club1,
            "home_venue": self.venue,
            "team_name": "team awesome",
            "home_day": "monday",
            "home_time": time(19, 0),
            "approved": True,
        }
        self.team = Team.objects.create(**self.team_data)

    def test_can_create_valid_season_player(self):
        """Verify TeamPlayer can be saved with valid data."""
        tp = TeamPlayer(
            player=self.player,
            team=self.team,
            paid_fees=True,
        )
        tp.full_clean()  # Should not raise error
        tp.save()
        self.assertTrue(TeamPlayer.objects.filter(id=tp.id).exists())

    def test_string_representation(self):
        tp = TeamPlayer.objects.create(player=self.player, team=self.team)
        expected_str = f"{self.player.full_name} ({self.team.team_name})"
        self.assertEqual(str(tp), expected_str)

    def test_ordering_by_player_surname_then_forename(self):
        # Create players in no particular order
        player_b = Player.objects.create(
            forename="Bob",
            surname="Anderson",
            date_of_birth=date(1992, 3, 3),
            current_club=self.club1,
            club_status="confirmed",
        )
        player_c = Player.objects.create(
            forename="Alice",
            surname="Smith",
            date_of_birth=date(1993, 4, 4),
            current_club=self.club1,
            club_status="confirmed",
        )
        # Create TeamPlayers
        tp_a = TeamPlayer.objects.create(player=self.player, team=self.team)
        tp_b = TeamPlayer.objects.create(player=player_b, team=self.team)
        tp_c = TeamPlayer.objects.create(player=player_c, team=self.team)

        players_ordered = list(TeamPlayer.objects.all())

        self.assertEqual(players_ordered[0], tp_b)
        self.assertEqual(players_ordered[1], tp_c)
        self.assertEqual(players_ordered[2], tp_a)

    def test_unique_player_and_season_constraint(self):
        """Verify that the same player and season cannot be duplicated."""
        # Create TeamPlayer
        TeamPlayer.objects.create(player=self.player, team=self.team)

        # Create TeamPlayer for same player in a different team
        different_team_data = self.team_data.copy()
        different_team_data["team_name"] = "A different team"
        different_team = Team.objects.create(**different_team_data)
        with self.assertRaises(ValidationError):
            tp = TeamPlayer.objects.create(
                player=self.player, team=different_team
            )
            tp.full_clean()

    # Validation tests
    def test_clean_raises_if_club_status_not_confirmed(self):
        """
        clean() should raise ValidationError if player's club_status is
        not confirmed.
        """
        player_pending = Player.objects.create(
            forename="John",
            surname="Snow",
            date_of_birth=date(1990, 1, 1),
            current_club=self.club1,
            club_status="pending",
        )
        tp = TeamPlayer(player=player_pending, team=self.team)
        with self.assertRaisesMessage(
            ValidationError,
            (
                "Club Admin must confirm that the player is associated with "
                "their club before proceeding."
            ),
        ):
            tp.full_clean()

    def test_clean_raises_if_clubs_do_not_match(self):
        """
        clean() should raise ValidationError if player's current_club
        doesn't match TeamPlayer club.
        """
        self.team.club = self.club2
        self.team.save()
        tp = TeamPlayer(player=self.player, team=self.team)
        with self.assertRaisesMessage(
            ValidationError,
            (
                "The player's profile states that they are not associated "
                "with the team club."
            ),
        ):
            tp.full_clean()

    def test_clean_passes_if_club_status_confirmed_and_clubs_match(self):
        """
        clean() should pass without errors if club_status is confirmed and
        clubs match.
        """
        tp = TeamPlayer(player=self.player, team=self.team)
        try:
            tp.full_clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly.")


class TeamTests(TestCase):
    """
    Unit tests for the Team model to verify field behaviour, validation,
    string representation, ordering, uniqueness, and deletion constraints.
    """

    def setUp(self):
        # Create clubs
        self.club = Club.objects.create(name="Test Club 1")

        # Create a player with confirmed club_status and club as current_club
        self.player = Player.objects.create(
            forename="John",
            surname="Doe",
            date_of_birth=date(1990, 1, 1),
            current_club=self.club,
            club_status="confirmed",
        )

        # Create Division - needed for season
        self.division = Division.objects.create(name="Division 1", rank=1)

        # Season data
        self.season_data_1 = {
            "name": "2024/25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }
        self.season_data_2 = {
            "name": "2025/26",
            "short_name": "25-26",
            "slug": "25-26",
            "start_date": date(2025, 9, 1),
            "end_date": date(2026, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2024, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2024, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }

        # Create seasons
        self.season1 = Season.objects.create(**self.season_data_1)
        self.season1.divisions.set([self.division])
        self.season1.save()
        self.season2 = Season.objects.create(**self.season_data_2)
        self.season2.divisions.set([self.division])
        self.season2.save()

        # Create Venue
        self.venue = Venue.objects.create(name="Test Venue 1")

        # Create Team
        self.team_data = {
            "season": self.season1,
            "division": self.division,
            "club": self.club,
            "home_venue": self.venue,
            "team_name": "team awesome",
            "home_day": "monday",
            "home_time": time(19, 0),
            "approved": True,
        }
        self.team = Team.objects.create(**self.team_data)

    def test_can_create_team(self):
        """Verify team can be saved and retrieved correctly."""
        self.team.full_clean()
        self.team.save()
        self.assertTrue(Team.objects.filter(id=self.team.id).exists())

    def test_string_representation(self):
        """
        Verify string representation returns 'team_name (season_short_name)'
        with title case.
        """
        self.team.save()
        self.assertEqual(str(self.team), "Team Awesome (24-25)")

    def test_ordering_by_team_name(self):
        """Verify teams are ordered by team name ascending."""
        Team.objects.all().delete()

        team1 = Team.objects.create(**self.team_data)
        team1.team_name = "C"
        team1.save()
        team2 = Team.objects.create(**self.team_data)
        team2.team_name = "A"
        team2.save()
        team3 = Team.objects.create(**self.team_data)
        team3.team_name = "B"
        team3.save()

        ordered_teams = list(Team.objects.all())
        self.assertEqual(ordered_teams[0], team2)
        self.assertEqual(ordered_teams[1], team3)
        self.assertEqual(ordered_teams[2], team1)

    # Multi-field tests
    def test_required_fields(self):
        """Verify whether each field is required or not"""
        required_fields = {
            "season": True,
            "division": True,
            "club": True,
            "home_venue": True,
            "team_name": True,
        }

        test_object = Team()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """Verify max length for team_name."""
        fields = {
            "team_name": 30,
        }

        # Check each field
        valid_data = self.team_data.copy()
        test_model = Team
        for field, max_length in fields.items():
            helper_test_max_length(
                self, test_model, valid_data, field, max_length
            )

    def test_unique_team_name_season(self):
        """Verify combination of team_name and season must be unique."""
        other_team_data = self.team_data.copy()
        other_team_data = {
            "season": self.season1,
            "division": self.division,
            "club": self.club,
            "home_venue": self.venue,
            "team_name": "team awesome",
            "home_day": "Another day",
            "home_time": time(19, 30),
            "approved": True,
        }
        with self.assertRaises(IntegrityError):
            Team.objects.create(**other_team_data)

    def test_can_create_teams_with_same_name_but_different_seasons(self):
        """
        Verify teams with same name but different season are allowed.
        """
        other_team_data = self.team_data.copy()
        other_team_data = {
            "season": self.season2,
            "division": self.division,
            "club": self.club,
            "home_venue": self.venue,
            "team_name": "team awesome",
            "home_day": "Another day",
            "home_time": time(19, 30),
            "approved": True,
        }
        other_team = Team.objects.create(**other_team_data)
        self.assertTrue(Team.objects.filter(id=other_team.id).exists())

    # Single-field tests
    def test_home_day_defaults_to_monday(self):
        """
        Verify home_day defaults to 'monday' if not provided.
        """
        Team.objects.all().delete()
        team_data = self.team_data.copy()
        del team_data["home_day"]
        team = Team.objects.create(**team_data)
        self.assertEqual(team.home_day, "monday")

    def test_home_time_defaults_to_7pm(self):
        """
        Verify home_time defaults to 7PM if not provided.
        """
        Team.objects.all().delete()
        team_data = self.team_data.copy()
        del team_data["home_time"]
        team = Team.objects.create(**team_data)
        self.assertEqual(team.home_time, time(19, 0))

    def test_home_time_validation_contraints(self):
        """Verify home_time must be between 6PM and 8PM."""
        # Too early - should raise validation error
        self.team.home_time = time(17, 59)
        with self.assertRaisesMessage(
            ValidationError, "Match must start between 6:00 PM and 8:00 PM."
        ):
            self.team.full_clean()

        # Earliest allowed start time - should pass without errors
        self.team.home_time = time(18, 0)
        self.team.full_clean()

        # Latest allowed start time - should pass without errors
        self.team.home_time = time(20, 0)
        self.team.full_clean()

        # Too late - should raise validation error
        self.team.home_time = time(20, 1)
        with self.assertRaisesMessage(
            ValidationError, "Match must start between 6:00 PM and 8:00 PM."
        ):
            self.team.full_clean()

    def test_division_can_not_be_changed_after_season_has_started(self):
        """Verify division cannot be changed after season start_date."""
        # Verify season start date for team is in the past
        now = timezone.now().date()
        self.assertTrue(self.team.season.start_date < now)

        # Changing division should raise validation error
        division2 = Division.objects.create(name="Division 2", rank=2)
        self.team.division = division2
        with self.assertRaises(ValidationError):
            self.team.full_clean()

    def test_division_can_be_changed_before_season_has_started(self):
        """Verify division can be changed before season start_date."""
        Team.objects.all().delete()

        # Create season with start date in the future
        now = timezone.now().date()
        season_data = {
            "name": "In the future",
            "short_name": "future",
            "slug": "future",
            "start_date": now + timezone.timedelta(days=10),
            "end_date": now + timezone.timedelta(days=50),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }
        season = Season.objects.create(**season_data)
        season.divisions.set([self.division])
        season.save()

        # Create team for this season
        team_data = self.team_data.copy()
        team_data["season"] = season
        team = Team.objects.create(**team_data)

        # Changing division should not raise validation error
        division2 = Division.objects.create(name="Division 2", rank=2)
        team.division = division2
        team.full_clean()


class FixtureTests(TestCase):
    """
    Unit tests for the Fixture model covering field behaviour, string
    representation, ordering, validation, and uniqueness constraints.
    """

    def setUp(self):
        # Create clubs
        self.club = Club.objects.create(name="Test Club 1")

        # Create Divisions - needed for season
        self.division1 = Division.objects.create(name="Division 1", rank=1)
        self.division2 = Division.objects.create(name="Division 2", rank=2)

        # Season data
        self.season_data_1 = {
            "name": "2024/25",
            "short_name": "24-25",
            "slug": "24-25",
            "start_date": date(2024, 9, 1),
            "end_date": date(2025, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2023, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2023, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }
        self.season_data_2 = {
            "name": "2025/26",
            "short_name": "25-26",
            "slug": "25-26",
            "start_date": date(2025, 9, 1),
            "end_date": date(2026, 5, 1),
            "registration_opens": timezone.make_aware(datetime(2024, 6, 1)),
            "registration_closes": timezone.make_aware(datetime(2024, 8, 1)),
            "is_visible": True,
            "is_current": True,
        }

        # Create seasons
        self.season1 = Season.objects.create(**self.season_data_1)
        self.season1.divisions.set([self.division1])
        self.season1.save()
        self.season2 = Season.objects.create(**self.season_data_2)
        self.season2.divisions.set([self.division1])
        self.season2.save()

        # Create Venue
        self.venue = Venue.objects.create(name="Test Venue 1")

        # Team data
        self.team_data1 = {
            "season": self.season1,
            "division": self.division1,
            "club": self.club,
            "home_venue": self.venue,
            "team_name": "Team A",
            "home_day": "monday",
            "home_time": time(19, 0),
            "approved": True,
        }
        self.team_data2 = {
            "season": self.season1,
            "division": self.division1,
            "club": self.club,
            "home_venue": self.venue,
            "team_name": "Team B",
            "home_day": "tuesday",
            "home_time": time(19, 0),
            "approved": True,
        }

        # Create teams
        self.team1 = Team.objects.create(**self.team_data1)
        self.team2 = Team.objects.create(**self.team_data2)

        # Create weeks
        self.week_season_1 = Week.objects.create(
            season=self.season1,
            name="Week 1 Season 1",
            details="",
            start_date=self.season1.start_date,
        )
        self.week_season_2 = Week.objects.create(
            season=self.season2,
            name="Week 1 Season 2",
            details="",
            start_date=self.season2.start_date,
        )

        # Fixture data
        self.fixture_data = {
            "season": self.season1,
            "division": self.division1,
            "week": self.week_season_1,
            "datetime": timezone.make_aware(datetime(2024, 9, 1, 19, 0)),
            "home_team": self.team1,
            "away_team": self.team2,
            "venue": self.venue,
            "status": "scheduled",
        }

    def test_can_create_fixture(self):
        """Verify a fixture can be saved and retrieved correctly."""
        fixture = Fixture.objects.create(**self.fixture_data)
        fixture.full_clean()
        fixture.save()
        self.assertTrue(Fixture.objects.filter(id=fixture.id).exists())

    def test_string_representation(self):
        """Verify string representation returns expected format."""
        fixture = Fixture.objects.create(**self.fixture_data)
        expected = (
            f"{fixture.season.short_name} {fixture.week.name} - "
            f"{fixture.home_team.team_name} vs {fixture.away_team.team_name}"
        )
        self.assertEqual(str(fixture), expected)

    def test_ordering_by_datetime(self):
        """Verify fixtures are ordered by datetime ascending."""
        # Create earlier fixture
        earlier_fixture = Fixture.objects.create(**self.fixture_data)

        # Create data for later fixture
        # Swap home / away team to avoid uniqueness constraint
        later_fixture_data = self.fixture_data.copy()
        later_fixture_data["home_team"] = self.team2
        later_fixture_data["away_team"] = self.team1

        later_fixture = Fixture.objects.create(**later_fixture_data)
        later_fixture.datetime = later_fixture.datetime + timezone.timedelta(
            days=1
        )
        later_fixture.save()

        ordered = list(Fixture.objects.all())
        self.assertEqual(ordered[0], earlier_fixture)
        self.assertEqual(ordered[1], later_fixture)

    # Multi-field tests
    def test_required_fields(self):
        """Verify whether each field is required or not"""
        required_fields = {
            "season": True,
            "division": True,
            "week": True,
            "datetime": True,
            "home_team": True,
            "away_team": True,
            "venue": False,
        }

        test_object = Fixture()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_unique_constraint_same_season_and_teams(self):
        """Ensure uniqueness constraint for season + home_team + away_team."""

        # Create fixture
        Fixture.objects.create(**self.fixture_data)

        # Create duplicate fixture - should raise error
        with self.assertRaises(IntegrityError):
            Fixture.objects.create(**self.fixture_data)

    def test_can_have_same_teams_in_different_season(self):
        """Verify can have same team pairing in a different season."""
        Fixture.objects.create(**self.fixture_data)

        # Create same teams in other season
        data_other_season_team1 = self.team_data1.copy()
        data_other_season_team1["season"] = self.season2
        other_season_team1 = Team.objects.create(**data_other_season_team1)

        data_other_season_team2 = self.team_data2.copy()
        data_other_season_team2["season"] = self.season2
        other_season_team2 = Team.objects.create(**data_other_season_team2)

        # Data for fixture in other season
        fixture_data2 = self.fixture_data.copy()
        fixture_data2["season"] = self.season2
        fixture_data2["week"] = self.week_season_2
        fixture_data2["datetime"] = timezone.make_aware(
            datetime(2025, 9, 1, 19, 0)
        )
        fixture_data2["home_team"] = other_season_team1
        fixture_data2["away_team"] = other_season_team2

        # Create fixture in other season - should not raise error
        fixture2 = Fixture.objects.create(**fixture_data2)
        fixture2.full_clean()
        self.assertTrue(Fixture.objects.filter(id=fixture2.id).exists())

    def test_clean_datetime_time_between_6pm_and_8pm(self):
        """
        Raise error if time part of datetime is outside of 6pm to 8pm range.
        """
        # Create fixture
        fixture = Fixture(**self.fixture_data)

        # Test a minute earlier than low end of range raises error
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 17, 59))
        with self.assertRaisesMessage(
            ValidationError, "Match must start between 6:00 PM and 8:00 PM."
        ):
            fixture.full_clean()

        # Test equal to low end of range is allowed
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 18, 00))
        fixture.full_clean()

        # Test equal to high end of range is allowed
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 20, 00))
        fixture.full_clean()

        # Test a minute after high end of range raises error
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 20, 1))
        with self.assertRaisesMessage(
            ValidationError, "Match must start between 6:00 PM and 8:00 PM."
        ):
            fixture.full_clean()

    def test_clean_datetime_date_within_week(self):
        """
        Raise error if time part of datetime is outside of 6pm to 8pm range.
        """
        # Create fixture
        fixture = Fixture(**self.fixture_data)

        # Test a minute earlier than low end of range raises error
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 17, 59))
        with self.assertRaisesMessage(
            ValidationError, "Match must start between 6:00 PM and 8:00 PM."
        ):
            fixture.full_clean()

        # Test equal to low end of range is allowed
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 18, 00))
        fixture.full_clean()

        # Test equal to high end of range is allowed
        fixture.datetime = timezone.make_aware(datetime(2024, 9, 1, 20, 00))
        fixture.full_clean()

        # Test a minute after high end of range raises error
        fixture.datetime = timezone.make_aware(datetime(2024, 10, 1, 20, 1))
        with self.assertRaisesMessage(
            ValidationError, "Match must start between 6:00 PM and 8:00 PM."
        ):
            fixture.full_clean()

    def test_clean_home_and_away_must_differ(self):
        """Raise error if a team is scheduled to play itself."""
        self.fixture_data["away_team"] = self.team1
        fixture = Fixture(**self.fixture_data)
        with self.assertRaisesMessage(
            ValidationError, "A team cannot play against itself."
        ):
            fixture.full_clean()

    def test_clean_teams_must_be_in_correct_division(self):
        """
        Verify validation error is raised if a team is in the wrong division.
        """
        self.team2.division = self.division2
        self.team2.save()

        fixture = Fixture(**self.fixture_data)
        with self.assertRaisesMessage(
            ValidationError, "Away team is not in the selected division."
        ):
            fixture.full_clean()

    def test_clean_teams_must_be_in_correct_season(self):
        """
        Verify validation error is raised if a team is in the wrong season.
        """
        self.team2.season = self.season2
        self.team2.save()

        fixture = Fixture(**self.fixture_data)
        with self.assertRaisesMessage(
            ValidationError, "Away team is not in the selected season."
        ):
            fixture.full_clean()
