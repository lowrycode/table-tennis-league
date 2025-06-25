from datetime import time
from django.test import TestCase
from django.core.exceptions import ValidationError
from league.forms import DoublesMatchAdminForm
from test_utils.helpers import (
    create_fixture_result_setup,
    create_player,
    create_team_player,
    create_season,
    create_team,
)


class DoublesMatchAdminFormTests(TestCase):
    """
    Tests for the DoublesMatchAdminForm to validate M2M fields
    (home_players and away_players).
    """

    def setUp(self):
        """
        Create FixtureResult (and related data), players and team players.
        """
        setup_data = create_fixture_result_setup()
        for key, value in setup_data.items():
            setattr(self, key, value)

        # Create players
        self.player1 = create_player("John", "Doe", self.club)
        self.player2 = create_player("Joe", "Bloggs", self.club)
        self.player3 = create_player("Anna", "Jones", self.club)
        self.player4 = create_player("Steve", "White", self.club)

        # Create team players
        self.tp1 = create_team_player(self.player1, self.team1)
        self.tp2 = create_team_player(self.player2, self.team1)
        self.tp3 = create_team_player(self.player3, self.team2)
        self.tp4 = create_team_player(self.player4, self.team2)

    def test_valid_form(self):
        """Verify form is valid with valid data"""
        form_data = {
            "fixture_result": self.fixture_result.id,
            "home_players": [self.tp1, self.tp2],
            "away_players": [self.tp3, self.tp4],
            "home_sets": 3,
            "away_sets": 1,
        }
        form = DoublesMatchAdminForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_home_players_must_be_two_players(self):
        """Verify exactly 2 players must be selected for home_players"""
        form_data = {
            "fixture_result": self.fixture_result.id,
            "home_players": [self.tp1],  # Only one player
            "away_players": [self.tp3, self.tp4],
            "home_sets": 3,
            "away_sets": 1,
        }
        form = DoublesMatchAdminForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("home_players", form.errors)
        self.assertEqual(
            form.errors["home_players"],
            ["Exactly 2 home players must be selected."],
        )

    def test_away_players_must_be_two_players(self):
        """Verify exactly 2 players must be selected for away_players"""
        form_data = {
            "fixture_result": self.fixture_result.id,
            "home_players": [self.tp1, self.tp2],
            "away_players": [self.tp3],  # Only one player
            "home_sets": 3,
            "away_sets": 1,
        }
        form = DoublesMatchAdminForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("away_players", form.errors)
        self.assertEqual(
            form.errors["away_players"],
            ["Exactly 2 away players must be selected."],
        )

    def test_player_cannot_be_on_both_teams(self):
        """Verify the same player cannot play in both teams"""
        form_data = {
            "fixture_result": self.fixture_result.id,
            "home_players": [self.tp1, self.tp2],
            "away_players": [self.tp1, self.tp3],  # player1 repeats
            "home_sets": 3,
            "away_sets": 1,
        }
        form = DoublesMatchAdminForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn(
            "A player cannot be on both teams.", form.errors["__all__"]
        )

    def test_home_player_wrong_season(self):
        """
        Verify a team player from another season cannot be assigned
        to home_players.
        """
        # Create a new season and a team in that season
        past_season = create_season(
            name="Past Season",
            short_name="20-21",
            slug="20-21",
            start_year=2020,
            end_year=2021,
            is_current=False,
            divisions_list=[self.division],
        )
        past_team = create_team(
            past_season,
            self.division,
            self.club,
            self.venue,
            "Past Team",
            "monday",
            time(19, 0),
        )

        # Create a player and assign them to the other team/season
        player = create_player("George", "Legend", self.club)
        past_tp = create_team_player(player, past_team)

        form_data = {
            "fixture_result": self.fixture_result.id,
            "home_players": [past_tp, self.tp2],
            "away_players": [self.tp3, self.tp4],
            "home_sets": 3,
            "away_sets": 1,
        }
        form = DoublesMatchAdminForm(data=form_data)
        with self.assertRaises(ValidationError):
            form.is_valid()
            form.clean()

    def test_away_player_wrong_season(self):
        """
        Verify a team player from another season cannot be assigned
        to away_players.
        """
        # Create a new season and a team in that season
        past_season = create_season(
            name="Past Season",
            short_name="20-21",
            slug="20-21",
            start_year=2020,
            end_year=2021,
            is_current=False,
            divisions_list=[self.division],
        )
        past_team = create_team(
            past_season,
            self.division,
            self.club,
            self.venue,
            "Past Team",
            "monday",
            time(19, 0),
        )

        # Create a player and assign them to the other team/season
        player = create_player("George", "Legend", self.club)
        past_tp = create_team_player(player, past_team)

        form_data = {
            "fixture_result": self.fixture_result.id,
            "home_players": [self.tp1, self.tp2],
            "away_players": [past_tp, self.tp4],
            "home_sets": 3,
            "away_sets": 1,
        }
        form = DoublesMatchAdminForm(data=form_data)
        with self.assertRaises(ValidationError):
            form.is_valid()
            form.clean()
