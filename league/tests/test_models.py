from datetime import date, datetime
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from test_utils.helpers import (
    helper_test_required_fields,
    helper_test_max_length,
)
from league.models import Division, Season, Week


class DivisionTests(TestCase):
    """
    Unit tests for the Division model to verify field behavior, validation,
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
        for field, max_length in fields.items():
            helper_test_max_length(
                self, Division, valid_data, field, max_length
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
    Unit tests for the Season model to verify field behavior, validation,
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
        for field, max_length in fields.items():
            helper_test_max_length(self, Season, valid_data, field, max_length)

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
    Unit tests for the Week model to verify field behavior, validation,
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
        valid_data = self.week_data
        for field, max_length in fields.items():
            helper_test_max_length(self, Week, valid_data, field, max_length)

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
