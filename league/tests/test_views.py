from datetime import time, datetime, timedelta
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from test_utils.helpers import (
    create_club,
    create_division,
    create_fixture,
    create_fixture_result,
    create_season,
    create_team,
    create_venue,
    create_week,
    delete_fixtures,
    delete_fixture_results,
    delete_team_players,
    delete_weeks,
    create_fixture_result_setup,
    create_player,
    create_team_player,
    create_singles_match,
    create_doubles_match,
    create_singles_game,
    create_doubles_game,
)


class FixturesPageTests(TestCase):
    def setUp(self):
        """Set up test data for the fixtures view tests."""

        # Clubs
        self.club1 = create_club("Test Club 1")
        self.club2 = create_club("Test Club 2")

        # Divisions
        self.division1 = create_division("Division 1", 1)
        self.division2 = create_division("Division 2", 2)

        # Seasons
        self.season1 = create_season(
            "2023/24",
            "23-24",
            "23-24",
            2023,
            2024,
            False,
            [self.division1, self.division2],
        )
        self.season2 = create_season(
            "2024/25",
            "24-25",
            "24-25",
            2024,
            2025,
            True,
            [self.division1, self.division2],
        )

        # Venues
        self.venue1 = create_venue("Test Venue 1")
        self.venue2 = create_venue("Test Venue 2")

        # Teams
        self.team1 = create_team(
            self.season1,
            self.division1,
            self.club1,
            self.venue1,
            "Team A Season 1",
            "monday",
            time(18, 0),
        )
        self.team2 = create_team(
            self.season1,
            self.division1,
            self.club1,
            self.venue1,
            "Team B Season 1",
            "tuesday",
            time(18, 15),
        )
        self.team3 = create_team(
            self.season1,
            self.division1,
            self.club2,
            self.venue2,
            "Team C Season 1",
            "wednesday",
            time(18, 30),
        )
        self.team4 = create_team(
            self.season1,
            self.division1,
            self.club2,
            self.venue2,
            "Team D Season 1",
            "thursday",
            time(18, 45),
        )

        self.team5 = create_team(
            self.season2,
            self.division1,
            self.club1,
            self.venue1,
            "Team A Season 2",
            "monday",
            time(19, 0),
        )
        self.team6 = create_team(
            self.season2,
            self.division1,
            self.club1,
            self.venue1,
            "Team B Season 2",
            "tuesday",
            time(19, 15),
        )
        self.team7 = create_team(
            self.season2,
            self.division1,
            self.club2,
            self.venue2,
            "Team C Season 2",
            "wednesday",
            time(19, 30),
        )
        self.team8 = create_team(
            self.season2,
            self.division1,
            self.club2,
            self.venue2,
            "Team D Season 2",
            "thursday",
            time(19, 45),
        )

        # Weeks
        self.week1_season1 = create_week(self.season1, 1)
        self.week2_season1 = create_week(self.season1, 2)
        self.week1_season2 = create_week(self.season2, 1)
        self.week2_season2 = create_week(self.season2, 2)

        # Fixtures
        self.fixture1 = create_fixture(
            self.season1,
            self.division1,
            self.week1_season1,
            self.team1,
            self.team2,
        )
        self.fixture2 = create_fixture(
            self.season1,
            self.division1,
            self.week1_season1,
            self.team3,
            self.team4,
        )
        self.fixture3 = create_fixture(
            self.season1,
            self.division1,
            self.week1_season1,
            self.team1,
            self.team3,
        )
        self.fixture4 = create_fixture(
            self.season1,
            self.division1,
            self.week1_season1,
            self.team2,
            self.team4,
        )

        self.fixture5 = create_fixture(
            self.season2,
            self.division1,
            self.week1_season2,
            self.team5,
            self.team6,
        )
        self.fixture6 = create_fixture(
            self.season2,
            self.division1,
            self.week1_season2,
            self.team7,
            self.team8,
        )
        self.fixture7 = create_fixture(
            self.season2,
            self.division1,
            self.week1_season2,
            self.team5,
            self.team7,
        )
        self.fixture8 = create_fixture(
            self.season2,
            self.division1,
            self.week1_season2,
            self.team6,
            self.team8,
        )

        self.url = reverse("fixtures")

    # Basic page details and context
    def test_fixtures_page_returns_200(self):
        """Verify valid response has status code 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_is_used(self):
        """Verify correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "league/fixtures.html")

    def test_page_contains_title_and_fixture_status_key(self):
        """Verify page contains title and fixture status colour key"""
        response = self.client.get(self.url)
        self.assertContains(response, "Fixtures</h1>")
        self.assertContains(response, 'id="fixture-status-key"')

    def test_context_contains_season_and_weeks(self):
        """Verify context contains current season and correct weeks."""
        response = self.client.get(self.url)
        self.assertIn("season", response.context)
        self.assertIn("weeks", response.context)
        self.assertEqual(response.context["season"], self.season2)
        self.assertEqual(len(response.context["weeks"]), 2)

    def test_weeks_are_ordered_by_start_date(self):
        """Verify weeks are ordered by start date in context."""
        response = self.client.get(self.url)
        weeks = list(response.context["weeks"])
        self.assertLess(weeks[0].start_date, weeks[1].start_date)

    # Fixtures details, status and fallbacks
    def test_week_details_are_displayed(self):
        """
        Verify week details include week name and start date.
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.week1_season2.name)
        self.assertContains(response, "Begins 1st Sep")

    def test_fixtures_details_are_displayed(self):
        """
        Verify details about fixture are displayed including:
        - team names
        - time
        - date
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.fixture5.home_team.team_name)
        self.assertContains(response, self.fixture5.away_team.team_name)
        self.assertContains(response, "Mon 2nd Sep")
        self.assertContains(response, "19:00")

    def test_fixtures_status_class_for_cancelled_fixture(self):
        """
        Verify .fixture-cancelled class is used when a fixture is cancelled.
        """
        # Cancel a fixture
        self.fixture5.status = "cancelled"
        self.fixture5.save()

        response = self.client.get(self.url)
        self.assertContains(response, '<li class="row fixture-cancelled">')

    def test_fixtures_status_class_for_postponed_fixture(self):
        """
        Verify .fixture-postponed class is used when a fixture is postponed.
        """
        # Postpone a fixture
        self.fixture5.status = "postponed"
        self.fixture5.save()

        response = self.client.get(self.url)
        self.assertContains(response, '<li class="row fixture-postponed">')

    def test_fixtures_status_class_for_completed_fixture(self):
        """
        Verify .fixture-completed class is used when a fixture is completed.
        """
        # Mark fixture as completed
        self.fixture5.status = "completed"
        self.fixture5.save()

        response = self.client.get(self.url)
        self.assertContains(response, '<li class="row fixture-completed">')

    def test_placeholder_displayed_when_no_current_season(self):
        """Verify placeholder is displayed when season is not found."""
        self.season2.is_current = False
        self.season2.save()

        response = self.client.get(self.url)
        self.assertContains(response, "Season not found.</p>")

    def test_placeholder_displayed_when_weeks_is_empty(self):
        """Verify placeholder is displayed when weeks is empty."""
        # Delete fixtures - needed due to protected foreign keys
        delete_fixtures()

        # Delete weeks
        delete_weeks()

        response = self.client.get(self.url)
        self.assertContains(response, "No weeks to display.</p>")

    def test_placeholder_displayed_when_weeks_has_no_fixtures(self):
        """Verify placeholder is displayed when a week has no fixtures."""
        delete_fixtures(week=self.week1_season1)

        response = self.client.get(self.url)
        self.assertContains(response, "No fixtures this week.</div>")

    def test_current_week_when_in_season(self):
        """
        Verify that current_week_id is passed from view, the template includes
        the 'Jump to Current Week' link and that a week section includes an id
        of 'current-week'
        """
        week_start = self.week2_season2.start_date
        test_date = datetime.combine(
            week_start + timedelta(days=2), datetime.min.time()
        )
        aware_test_date = timezone.make_aware(test_date)

        with patch("league.views.timezone.now", return_value=aware_test_date):
            response = self.client.get(self.url)
            current_week_id = response.context.get("current_week_id")

            self.assertEqual(current_week_id, self.week2_season2.id)
            self.assertContains(response, "Jump to Current Week")
            self.assertContains(response, 'id="current-week"')

    def test_current_week_when_out_of_season(self):
        """
        Verify that current_week_id is passed as None from the view, the
        template does not include the 'Jump to Current Week' link and that
        id='current-week' is not found
        """
        week_start = self.week1_season1.start_date
        test_date = datetime.combine(
            week_start - timedelta(days=20), datetime.min.time()
        )
        aware_test_date = timezone.make_aware(test_date)

        with patch("league.views.timezone.now", return_value=aware_test_date):
            response = self.client.get(self.url)
            current_week_id = response.context.get("current_week_id")

            self.assertIsNone(current_week_id)
            self.assertNotContains(response, "Jump to Current Week")
            self.assertNotContains(response, 'id="current-week"')

    # Filters and HTMX
    def test_context_contains_filter_and_filters_applied(self):
        """Verify context contains filter and filters_applied."""
        response = self.client.get(self.url)
        self.assertIn("filter", response.context)
        self.assertIn("filters_applied", response.context)

    def test_htmx_request_returns_partial_template(self):
        """Verify HTMX requests return the fixtures section partial."""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertTemplateUsed(
            response, "league/partials/fixtures_section.html"
        )

    def test_htmx_season_filtering_updates_fixtures(self):
        """Verify HTMX request with season filter updated the fixture list."""
        response = self.client.get(
            self.url, {"season": self.season1.slug}, HTTP_HX_REQUEST="true"
        )

        # Should contain team from season 1
        self.assertContains(response, self.fixture1.home_team.team_name)

        # Should not contain team from season 2
        self.assertNotContains(response, self.fixture5.home_team.team_name)

    def test_htmx_invalid_season_renders_correct_placeholder(self):
        """
        Verify an invalid season slug results in context["season]=None
        and placeholder being displayed.
        """
        response = self.client.get(
            self.url, {"season": "non-existent"}, HTTP_HX_REQUEST="true"
        )
        self.assertIsNone(response.context["season"])
        self.assertContains(response, "Season not found.")

    def test_htmx_invisible_season_renders_correct_placeholder(self):
        """
        Verify a season with is_visible=False results in context["season]=None
        and placeholder being displayed.
        """
        invisible_season = create_season(
            "Invisible", "20-21", "20-21", 2020, 2021, False, [self.division1]
        )
        invisible_season.is_visible = False
        invisible_season.save()

        response = self.client.get(
            self.url, {"season": invisible_season.slug}, HTTP_HX_REQUEST="true"
        )
        self.assertIsNone(response.context["season"])
        self.assertContains(response, "Season not found.")

    def test_htmx_division_filter_returns_correct_fixtures(self):
        """Verify HTMX request with division filter updates fixture list."""
        # Create teams and fixture for division 2 in season 2 (current)
        div2_team1 = create_team(
            self.season2,
            self.division2,
            self.club1,
            self.venue1,
            "Team 1 Division 2",
            "monday",
            time(18, 0),
        )
        div2_team2 = create_team(
            self.season2,
            self.division2,
            self.club1,
            self.venue1,
            "Team 2 Division 2",
            "monday",
            time(18, 0),
        )
        div2_fixture = create_fixture(
            self.season2,
            self.division2,
            self.week1_season2,
            div2_team1,
            div2_team2,
        )

        response = self.client.get(
            self.url,
            {
                "division": self.division2.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include fixture from division2 season 2
        self.assertContains(response, div2_fixture.home_team.team_name)
        self.assertContains(response, div2_fixture.away_team.team_name)

        # Should not contain fixtures from division1 season1
        self.assertNotContains(response, self.fixture1.home_team.team_name)

        # Should not contain fixtures from division1 season2
        self.assertNotContains(response, self.fixture5.home_team.team_name)

    def test_htmx_season_and_division_filters_together(self):
        """
        Verify HTMX request with both season and division filters update
        fixture list correctly.
        """
        # Create teams and fixture for division 2 in season 1
        div2_team1 = create_team(
            self.season1,
            self.division2,
            self.club1,
            self.venue1,
            "Team1 S1 D2",
            "monday",
            time(18, 0),
        )
        div2_team2 = create_team(
            self.season1,
            self.division2,
            self.club1,
            self.venue1,
            "Team2 S1 D2",
            "monday",
            time(18, 0),
        )
        d2_s1_fixture = create_fixture(
            self.season1,
            self.division2,
            self.week1_season1,
            div2_team1,
            div2_team2,
        )

        # Create teams and fixture for division 2 in season 2
        div2_team3 = create_team(
            self.season2,
            self.division2,
            self.club1,
            self.venue1,
            "Team3 S2 D2",
            "monday",
            time(18, 0),
        )
        div2_team4 = create_team(
            self.season2,
            self.division2,
            self.club1,
            self.venue1,
            "Team4 S2 D2",
            "monday",
            time(18, 0),
        )
        d2_s2_fixture = create_fixture(
            self.season2,
            self.division2,
            self.week1_season2,
            div2_team3,
            div2_team4,
        )

        response = self.client.get(
            self.url,
            {
                "season": self.season1.slug,
                "division": self.division2.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include fixture from division2 season 1
        self.assertContains(response, d2_s1_fixture.home_team.team_name)
        self.assertContains(response, d2_s1_fixture.away_team.team_name)

        # Should not contain fixtures from division2 season 2
        self.assertNotContains(response, d2_s2_fixture.home_team.team_name)
        self.assertNotContains(response, d2_s2_fixture.home_team.team_name)

        # Should not contain fixtures from division1 season 1
        self.assertNotContains(response, self.fixture1.home_team.team_name)

        # Should not contain fixtures from division1 season 2
        self.assertNotContains(response, self.fixture5.home_team.team_name)

    def test_htmx_club_filter_returns_club_home_fixtures(self):
        """
        Verify HTMX request with club filter includes fixtures where
        club team is playing at home
        """

        # Delete fixtures
        delete_fixtures()

        # Create fixture where neither home or away team in club
        fixture_neither_in_club = create_fixture(
            self.season2,
            self.division1,
            self.week1_season2,
            self.team7,
            self.team8,
        )

        # Create fixture where home team in club but not away team
        fixture_home_in_club = create_fixture(
            self.season2,
            self.division1,
            self.week2_season2,
            self.team5,
            self.team7,
        )

        response = self.client.get(
            self.url,
            {
                "season": self.season2.slug,
                "club": self.club1.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include teams in fixtures where home team is in specified club
        self.assertContains(response, fixture_home_in_club.home_team.team_name)
        self.assertContains(response, fixture_home_in_club.away_team.team_name)

        # Should not include teams which do not play against club teams
        self.assertNotContains(
            response, fixture_neither_in_club.away_team.team_name
        )

    def test_htmx_club_filter_returns_club_away_fixtures(self):
        """
        Verify HTMX request with club filter includes fixtures where
        club team is playing away
        """

        # Delete fixtures
        delete_fixtures()

        # Create fixture where neither home or away team in club
        fixture_neither_in_club = create_fixture(
            self.season2,
            self.division1,
            self.week1_season2,
            self.team7,
            self.team8,
        )

        # Create fixture where away team in club but not home team
        fixture_home_in_club = create_fixture(
            self.season2,
            self.division1,
            self.week2_season2,
            self.team7,
            self.team5,
        )

        response = self.client.get(
            self.url,
            {
                "season": self.season2.slug,
                "club": self.club1.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include teams in fixtures where away team is in specified club
        self.assertContains(response, fixture_home_in_club.home_team.team_name)
        self.assertContains(response, fixture_home_in_club.away_team.team_name)

        # Should not include teams which do not play against club teams
        self.assertNotContains(
            response, fixture_neither_in_club.away_team.team_name
        )


class FixturesFilterView(TestCase):
    def setUp(self):
        """Define url for tests"""
        self.url = reverse("fixtures_filter")

    def test_valid_htmx_requests_renders_correct_partial(self):
        """Verify correct template is rendered for HTMX request"""
        response = self.client.get(
            self.url,
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "league/partials/fixtures_filter_panel_inner.html"
        )

    def test_non_htmx_requests_return_bad_request(self):
        """Verify Bad Request status 400 returned for non-HTMX requests"""
        response = self.client.get(self.url)
        self.assertContains(response, "HTMX requests only", status_code=400)


class ResultsPageTests(TestCase):
    def setUp(self):
        """Set up test data for the results view tests."""

        # Create a fixture with result using helper method
        setup_data = create_fixture_result_setup()

        # Assign to self
        for key, value in setup_data.items():
            setattr(self, key, value)

        self.url = reverse("results")

    # Basic page details and context
    def test_results_page_returns_200(self):
        """Verify valid response has status code 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_is_used(self):
        """Verify correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "league/results.html")

    def test_page_contains_title(self):
        """Verify page contains title"""
        response = self.client.get(self.url)
        self.assertContains(response, "Results</h1>")

    def test_context_contains_season_and_weeks(self):
        """Verify context contains current season and correct weeks."""
        # Create another week
        week2 = create_week(season=self.season, week_num=2)

        # Create fixture without result
        # (teams reversed to avoid unique constraint)
        create_fixture(
            self.season, self.division, week2, self.team2, self.team1
        )

        response = self.client.get(self.url)
        self.assertIn("season", response.context)
        self.assertIn("weeks", response.context)
        self.assertEqual(response.context["season"], self.season)
        # no results in second week so should not be included
        self.assertEqual(len(response.context["weeks"]), 1)

    def test_weeks_are_ordered_by_start_date_desc(self):
        """Verify weeks are reverse ordered by start date in context."""
        # Create another week
        week2 = create_week(season=self.season, week_num=2)

        # Create fixture with result
        # (teams reversed to avoid unique constraint)
        fixture2 = create_fixture(
            self.season, self.division, week2, self.team2, self.team1
        )
        create_fixture_result(fixture2, 8, 2)

        response = self.client.get(self.url)
        weeks = list(response.context["weeks"])
        self.assertEqual(len(weeks), 2)
        self.assertGreater(weeks[0].start_date, weeks[1].start_date)

    # Fixtures details, status and fallbacks
    def test_week_details_are_displayed(self):
        """
        Verify week details include week name and start date.
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.week.name)
        self.assertContains(response, "Begins 1st Sep")

    def test_results_details_are_displayed(self):
        """
        Verify details about fixture result are displayed including:
        - team names
        - date
        - score
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.fixture.home_team.team_name)
        self.assertContains(response, self.fixture.away_team.team_name)
        self.assertContains(response, "Mon 2nd Sep")
        self.assertContains(
            response,
            (
                f"{self.fixture.result.home_score} - "
                f"{self.fixture.result.away_score}"
            ),
        )

    def test_placeholder_displayed_when_no_current_season(self):
        """Verify placeholder is displayed when season is not found."""
        self.season.is_current = False
        self.season.save()

        response = self.client.get(self.url)
        self.assertContains(response, "Season not found.</p>")

    def test_placeholder_displayed_when_weeks_is_empty(self):
        """Verify placeholder is displayed when weeks is empty."""
        # Delete fixtures - needed due to protected foreign keys
        delete_fixtures()

        # Delete weeks
        delete_weeks()

        response = self.client.get(self.url)
        self.assertContains(response, "No results to display.</p>")

    # Filters and HTMX
    def test_context_contains_filter_and_filters_applied(self):
        """Verify context contains filter and filters_applied."""
        response = self.client.get(self.url)
        self.assertIn("filter", response.context)
        self.assertIn("filters_applied", response.context)

    def test_htmx_request_returns_partial_template(self):
        """Verify HTMX requests return the results section partial."""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertTemplateUsed(
            response, "league/partials/results_section.html"
        )

    def test_htmx_season_filtering_updates_results_list(self):
        """Verify HTMX request with season filter updates the results list."""
        # Create fixture and result for past season
        past_season = create_season(
            "Past Season", "20-21", "20-21", 2020, 2021, False, [self.division]
        )
        past_week = create_week(past_season, 1)
        past_team1 = create_team(
            season=past_season,
            division=self.division,
            club=self.club,
            venue=self.venue,
            team_name="Team C Past",
            home_day="monday",
            home_time=time(19, 0),
        )
        past_team2 = create_team(
            season=past_season,
            division=self.division,
            club=self.club,
            venue=self.venue,
            team_name="Team D Past",
            home_day="tuesday",
            home_time=time(19, 0),
        )

        past_fixture = create_fixture(
            season=past_season,
            division=self.division,
            week=past_week,
            home_team=past_team1,
            away_team=past_team2,
        )

        create_fixture_result(
            fixture=past_fixture,
            home_score=7,
            away_score=3,
        )

        response = self.client.get(
            self.url, {"season": past_season.slug}, HTTP_HX_REQUEST="true"
        )

        # Should contain team from past season
        self.assertContains(response, past_team1.team_name)

        # Should not contain team from current season
        self.assertNotContains(response, self.fixture.home_team.team_name)

    def test_htmx_invalid_season_renders_correct_placeholder(self):
        """
        Verify an invalid season slug results in context["season]=None
        and placeholder being displayed.
        """
        response = self.client.get(
            self.url, {"season": "non-existent"}, HTTP_HX_REQUEST="true"
        )
        self.assertIsNone(response.context["season"])
        self.assertContains(response, "Season not found.")

    def test_htmx_invisible_season_renders_correct_placeholder(self):
        """
        Verify a season with is_visible=False results in context["season]=None
        and placeholder being displayed.
        """
        invisible_season = create_season(
            "Invisible", "20-21", "20-21", 2020, 2021, False, [self.division]
        )
        invisible_season.is_visible = False
        invisible_season.save()

        response = self.client.get(
            self.url, {"season": invisible_season.slug}, HTTP_HX_REQUEST="true"
        )
        self.assertIsNone(response.context["season"])
        self.assertContains(response, "Season not found.")

    def test_htmx_division_filter_returns_correct_results(self):
        """Verify HTMX request with division filter updates results list."""
        # Create teams, fixture and result for division 2 in current season
        division2 = create_division("Division 2", 2)
        self.season.divisions.set([self.division, division2])
        div2_team1 = create_team(
            self.season,
            division2,
            self.club,
            self.venue,
            "Team 1 Division 2",
            "monday",
            time(18, 0),
        )
        div2_team2 = create_team(
            self.season,
            division2,
            self.club,
            self.venue,
            "Team 2 Division 2",
            "monday",
            time(18, 0),
        )
        div2_fixture = create_fixture(
            self.season,
            division2,
            self.week,
            div2_team1,
            div2_team2,
        )

        create_fixture_result(
            fixture=div2_fixture,
            home_score=7,
            away_score=3,
        )

        response = self.client.get(
            self.url,
            {
                "division": division2.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include fixture result from division2
        self.assertContains(response, div2_fixture.home_team.team_name)
        self.assertContains(response, div2_fixture.away_team.team_name)

        # Should not contain fixture results from division1
        self.assertNotContains(response, self.fixture.home_team.team_name)

    def test_htmx_season_and_division_filters_together(self):
        """
        Verify HTMX request with both season and division filters update
        results list correctly.
        """
        # Add division 2 to current season
        division1 = self.division
        division2 = create_division("Division 2", 2)
        self.season.divisions.set([division1, division2])

        # Add past season and past week
        past_season = create_season(
            "Past Season",
            "20-21",
            "20-21",
            2020,
            2021,
            False,
            [division1, division2],
        )
        past_week = create_week(past_season, 1)

        # Add Past teams from both divisions
        past_div1_team1 = create_team(
            season=past_season,
            division=division1,
            club=self.club,
            venue=self.venue,
            team_name="Past Team1 Div1",
            home_day="monday",
            home_time=time(19, 0),
        )
        past_div1_team2 = create_team(
            season=past_season,
            division=division1,
            club=self.club,
            venue=self.venue,
            team_name="Past Team2 Div1",
            home_day="tuesday",
            home_time=time(19, 0),
        )
        past_div2_team1 = create_team(
            season=past_season,
            division=division2,
            club=self.club,
            venue=self.venue,
            team_name="Past Team1 Div2",
            home_day="monday",
            home_time=time(19, 0),
        )
        past_div2_team2 = create_team(
            season=past_season,
            division=division2,
            club=self.club,
            venue=self.venue,
            team_name="Past Team2 Div2",
            home_day="tuesday",
            home_time=time(19, 0),
        )

        # Add past fixtures and results
        past_div1_fixture = create_fixture(
            past_season,
            division1,
            past_week,
            past_div1_team1,
            past_div1_team2,
        )
        create_fixture_result(
            fixture=past_div1_fixture,
            home_score=7,
            away_score=3,
        )

        past_div2_fixture = create_fixture(
            past_season,
            division2,
            past_week,
            past_div2_team1,
            past_div2_team2,
        )
        create_fixture_result(
            fixture=past_div2_fixture,
            home_score=7,
            away_score=3,
        )

        response = self.client.get(
            self.url,
            {
                "season": past_season.slug,
                "division": division1.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include fixture results from division1 past season
        self.assertContains(response, past_div1_fixture.home_team.team_name)
        self.assertContains(response, past_div1_fixture.away_team.team_name)

        # Should not contain fixture results from division2 past season
        self.assertNotContains(response, past_div2_fixture.home_team.team_name)
        self.assertNotContains(response, past_div2_fixture.home_team.team_name)

        # Should not contain fixture results from division1 current season
        self.assertNotContains(response, self.fixture.home_team.team_name)
        self.assertNotContains(response, self.fixture.away_team.team_name)

    def test_htmx_club_filter_returns_club_home_fixture_results(self):
        """
        Verify HTMX request with club filter includes fixture results where
        club team is playing at home
        """

        # Delete fixtures and associated results
        delete_fixtures()

        foreign_club = create_club("Some other club")
        foreign_team1 = create_team(
            self.season,
            self.division,
            foreign_club,
            self.venue,
            "Foreign Team 1",
            "monday",
            time(18, 0),
        )
        foreign_team2 = create_team(
            self.season,
            self.division,
            foreign_club,
            self.venue,
            "Foreign Team 2",
            "monday",
            time(18, 0),
        )

        # Create fixture and result where neither home or away team in club
        fixture_neither_in_club = create_fixture(
            self.season,
            self.division,
            self.week,
            foreign_team1,
            foreign_team2,
        )
        create_fixture_result(fixture_neither_in_club, 7, 3)

        # Create fixture and result where home team in club but not away team
        fixture_home_in_club = create_fixture(
            self.season,
            self.division,
            self.week,
            self.team1,
            foreign_team1,
        )
        create_fixture_result(fixture_home_in_club, 7, 3)

        response = self.client.get(
            self.url,
            {
                "season": self.season.slug,
                "club": self.club.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include teams in fixtures where home team is in specified club
        self.assertContains(response, fixture_home_in_club.home_team.team_name)
        self.assertContains(response, fixture_home_in_club.away_team.team_name)

        # Should not include teams which do not play against club teams
        self.assertNotContains(
            response, fixture_neither_in_club.away_team.team_name
        )

    def test_htmx_club_filter_returns_club_away_fixture_results(self):
        """
        Verify HTMX request with club filter includes results where
        club team is playing away
        """

        # Delete fixtures and associated results
        delete_fixtures()

        foreign_club = create_club("Some other club")
        foreign_team1 = create_team(
            self.season,
            self.division,
            foreign_club,
            self.venue,
            "Foreign Team 1",
            "monday",
            time(18, 0),
        )
        foreign_team2 = create_team(
            self.season,
            self.division,
            foreign_club,
            self.venue,
            "Foreign Team 2",
            "monday",
            time(18, 0),
        )

        # Create fixture and result where neither home or away team in club
        fixture_neither_in_club = create_fixture(
            self.season,
            self.division,
            self.week,
            foreign_team1,
            foreign_team2,
        )
        create_fixture_result(fixture_neither_in_club, 7, 3)

        # Create fixture and result where home team in club but not away team
        fixture_home_in_club = create_fixture(
            self.season,
            self.division,
            self.week,
            foreign_team1,
            self.team1,
        )
        create_fixture_result(fixture_home_in_club, 7, 3)

        response = self.client.get(
            self.url,
            {
                "season": self.season.slug,
                "club": self.club.id,
            },
            HTTP_HX_REQUEST="true",
        )

        # Should include teams in fixtures where away team is in specified club
        self.assertContains(response, fixture_home_in_club.home_team.team_name)
        self.assertContains(response, fixture_home_in_club.away_team.team_name)

        # Should not include teams which do not play against club teams
        self.assertNotContains(
            response, fixture_neither_in_club.away_team.team_name
        )


class ResultBreakdownPageTests(TestCase):
    def setUp(self):
        """Create test data for result_breakdown view."""

        # Create a fixture with result using helper method
        setup_data = create_fixture_result_setup()

        # Assign to self
        for key, value in setup_data.items():
            setattr(self, key, value)

        # Create players
        self.player1 = create_player("Player", "One", self.club)
        self.player2 = create_player("Player", "Two", self.club)
        self.player3 = create_player("Player", "Three", self.club)
        self.player4 = create_player("Player", "Four", self.club)

        # Create team players
        self.home_player1 = create_team_player(self.player1, self.team1)
        self.home_player2 = create_team_player(self.player2, self.team1)
        self.away_player1 = create_team_player(self.player3, self.team2)
        self.away_player2 = create_team_player(self.player4, self.team2)

        # Create singles matches
        self.sm1 = create_singles_match(
            self.fixture_result, self.home_player1, self.away_player1, 3, 0
        )
        self.sm2 = create_singles_match(
            self.fixture_result, self.home_player1, self.away_player2, 1, 3
        )

        # Create doubles match
        self.dm = create_doubles_match(
            self.fixture_result,
            [self.home_player1, self.home_player2],
            [self.away_player1, self.away_player2],
            3,
            2,
        )

        self.url = reverse("result_breakdown", args=[self.fixture.id])

    def test_view_returns_200_with_valid_fixture(self):
        """Verify the result breakdown page returns status code 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Verify the correct template is used for the result breakdown."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "league/result_breakdown.html")

    def test_redirect_if_no_result(self):
        """
        Verify redirects to 'results' if fixture has no result with a
        warning message.
        """
        # Remove result from fixture
        self.fixture.result.delete()
        # self.fixture.save()

        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse("results"))

        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "No result found for this fixture",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.WARNING)

    def test_context_contains_fixture_and_win_counts(self):
        """
        Verify context includes fixture and player win counts dictionaries.
        """
        response = self.client.get(self.url)
        self.assertIn("fixture", response.context)
        self.assertIn("home_player_win_counts", response.context)
        self.assertIn("away_player_win_counts", response.context)

        # The fixture should be the same as test fixture
        self.assertEqual(response.context["fixture"], self.fixture)

    def test_home_player_win_counts_correct(self):
        """Verify home player wins are counted correctly."""
        response = self.client.get(self.url)
        home_win_counts = response.context["home_player_win_counts"]

        # Home player 1 should have 1 win from singles_match
        self.assertIn(self.home_player1.player, home_win_counts)
        self.assertEqual(home_win_counts[self.home_player1.player], 1)

    def test_away_player_win_counts_correct(self):
        """Verify away player wins are counted correctly."""
        response = self.client.get(self.url)
        away_win_counts = response.context["away_player_win_counts"]

        self.assertIn(self.away_player2.player, away_win_counts)
        self.assertEqual(away_win_counts[self.away_player2.player], 1)

    def test_away_player_win_counts_excludes_losers(self):
        """
        Verify away player with no wins is not found in away_player_win_counts.
        """
        response = self.client.get(self.url)
        away_win_counts = response.context["away_player_win_counts"]

        self.assertNotIn(self.away_player1.player, away_win_counts)

    def test_template_displays_fixture_details(self):
        """
        Verify template renders fixture date, venue, time, team names
        and scores.
        """
        response = self.client.get(self.url)

        # Check fixture info in response content
        self.assertContains(response, self.fixture.datetime.strftime("%a"))
        self.assertContains(response, self.venue.name)
        self.assertContains(response, self.fixture.datetime.strftime("%H:%M"))
        self.assertContains(response, self.team1.team_name)
        self.assertContains(response, self.team2.team_name)
        self.assertContains(response, self.fixture.result.home_score)
        self.assertContains(response, self.fixture.result.away_score)

    def test_template_displays_home_and_away_player_wins(self):
        """Verify template renders home and away player win counts."""
        response = self.client.get(self.url)

        # Player full names should appear with win counts
        self.assertContains(
            response, f"{self.home_player1.player.full_name} 1"
        )
        self.assertContains(
            response, f"{self.away_player2.player.full_name} 1"
        )

    def test_template_lists_singles_match_scores(self):
        """Verify template lists set scores for singles matches."""
        response = self.client.get(self.url)

        # Check match scores appear
        self.assertContains(
            response, f"{self.sm1.home_sets} - {self.sm1.away_sets}"
        )
        self.assertContains(
            response, f"{self.sm2.home_sets} - {self.sm2.away_sets}"
        )

    def test_template_lists_singles_game_scores(self):
        """Verify template lists singles game scores."""
        # Create singles_games
        create_singles_game(self.sm1, 1, 11, 3)
        create_singles_game(self.sm1, 2, 11, 5)
        create_singles_game(self.sm1, 3, 11, 7)

        response = self.client.get(self.url)

        # Check game scores appear
        self.assertContains(response, "11-3")
        self.assertContains(response, "11-5")
        self.assertContains(response, "11-7")

    def test_template_handles_no_singles_matches(self):
        """Verify placeholder text is displayed if no singles matches."""
        # Remove singles matches
        self.fixture_result.singles_matches.all().delete()
        response = self.client.get(self.url)
        self.assertContains(
            response, "No scores for the singles matches have been recorded."
        )

    def test_template_handles_no_singles_game_scores(self):
        """
        Verify placeholder text displays if no games scores are recorded for
        a singles match.
        """
        # Remove doubles match (this has no game scores either)
        self.fixture_result.doubles_match.delete()

        response = self.client.get(self.url)
        self.assertContains(response, "No game scores recorded")

    def test_template_handles_no_doubles_match(self):
        """Verify placeholder text is displayed if no doubles match."""
        self.fixture_result.doubles_match.delete()
        response = self.client.get(self.url)
        self.assertContains(
            response, "No scores for the doubles match have been recorded."
        )

    def test_template_lists_doubles_match_with_players_and_scores(self):
        """Template lists doubles match details when present."""
        # Delete singles matches
        self.fixture.result.singles_matches.all().delete()

        response = self.client.get(self.url)

        # Check doubles match players and scores appear
        self.assertContains(response, "<span>+</span>")
        self.assertContains(response, "<span>Player One</span>")
        self.assertContains(response, "<span>Player Two</span>")
        self.assertContains(response, "<span>Player Three</span>")
        self.assertContains(response, "<span>Player Four</span>")
        self.assertContains(response, "3 - 2")

    def test_template_lists_doubles_game_scores(self):
        """Verify template lists doubles game scores."""
        # Create doubles_games
        create_doubles_game(self.dm, 1, 11, 3)
        create_doubles_game(self.dm, 2, 11, 5)
        create_doubles_game(self.dm, 3, 11, 7)

        response = self.client.get(self.url)

        # Check game scores appear
        self.assertContains(response, "11-3")
        self.assertContains(response, "11-5")
        self.assertContains(response, "11-7")

    def test_template_handles_no_doubles_game_scores(self):
        """
        Verify placeholder text displays if no games scores are recorded for
        the doubles match.
        """
        # Remove singles matches (these have no game scores either)
        self.fixture_result.singles_matches.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, "No game scores recorded")


class TablesPageTests(TestCase):
    def setUp(self):
        """Create test data."""
        # Clubs and venues
        self.club = create_club("Test Club")
        self.venue = create_venue("Venue 1")

        # Divisions
        self.division1 = create_division(name="Division 1", rank=1)
        self.division2 = create_division(name="Division 2", rank=2)

        # Seasons
        self.season1 = create_season(
            name="2023/24",
            short_name="23-24",
            slug="23-24",
            start_year=2023,
            end_year=2024,
            is_current=False,
            divisions_list=[self.division1, self.division2],
        )
        self.season2 = create_season(
            name="2024/25",
            short_name="24-25",
            slug="24-25",
            start_year=2024,
            end_year=2025,
            is_current=True,
            divisions_list=[self.division1, self.division2],
        )

        # Teams - 3 in each division in active season
        self.s2_d1_team1 = create_team(
            season=self.season2,
            division=self.division1,
            club=self.club,
            venue=self.venue,
            team_name="s2 d1 t1",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.s2_d1_team2 = create_team(
            season=self.season2,
            division=self.division1,
            club=self.club,
            venue=self.venue,
            team_name="s2 d1 t2",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.s2_d1_team3 = create_team(
            season=self.season2,
            division=self.division1,
            club=self.club,
            venue=self.venue,
            team_name="s2 d1 t3",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.s2_d2_team1 = create_team(
            season=self.season2,
            division=self.division2,
            club=self.club,
            venue=self.venue,
            team_name="s2 d2 t1",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.s2_d2_team2 = create_team(
            season=self.season2,
            division=self.division2,
            club=self.club,
            venue=self.venue,
            team_name="s2 d2 t2",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.s2_d2_team3 = create_team(
            season=self.season2,
            division=self.division2,
            club=self.club,
            venue=self.venue,
            team_name="s2 d2 t3",
            home_day="monday",
            home_time=time(19, 0),
        )

        # Weeks - 3 in current season
        self.week1 = create_week(season=self.season2, week_num=1)
        self.week2 = create_week(season=self.season2, week_num=2)
        self.week3 = create_week(season=self.season2, week_num=3)

        self.url = reverse("tables")

    def test_tables_page_loads_successfully(self):
        """Veryify status code 200 for tables page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_tables_page_uses_correct_template(self):
        """Verify correct template is used for tables page."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "league/tables.html")

    def test_tables_page_context_includes_season_and_divisions(self):
        """Verify context includes current season and division_teams."""
        response = self.client.get(self.url)

        self.assertIn("season", response.context)
        self.assertEqual(response.context["season"], self.season2)

        self.assertIn("division_tables", response.context)
        self.assertEqual(len(response.context["division_tables"]), 2)

    def test_tables_page_displays_divisions_in_rank_order(self):
        """Verify divisions are ordered by rank."""
        response = self.client.get(self.url)
        content = response.content.decode("utf-8")

        d1_index = content.find("Division 1")
        d2_index = content.find("Division 2")

        self.assertLess(d1_index, d2_index)

    def test_tables_page_handles_no_current_season(self):
        """Verify placeholder displayed when season not found."""
        self.season2.is_current = False
        self.season2.save()

        response = self.client.get(self.url)
        self.assertContains(response, "Season not found")

    def test_tables_page_handles_seasons_with_no_divisions(self):
        """Verify placeholder displayed when season has no divisions."""
        self.season2.divisions.set([])
        response = self.client.get(self.url)
        self.assertContains(response, "No tables to display")

    def test_tables_displays_teams_without_fixtures(self):
        """
        Verify teams are displayed in the table even if have no fixtures yet.
        """
        response = self.client.get(reverse("tables"))
        content = response.content.decode("utf-8")

        # Teams in division 1 (current season)
        self.assertIn(self.s2_d1_team1.team_name, content)
        self.assertIn(self.s2_d1_team2.team_name, content)
        self.assertIn(self.s2_d1_team3.team_name, content)

        # Teams in division 2 (current season)
        self.assertIn(self.s2_d2_team1.team_name, content)
        self.assertIn(self.s2_d2_team2.team_name, content)
        self.assertIn(self.s2_d2_team3.team_name, content)

    def test_context_sorts_teams_by_points(self):
        """
        Verify teams are sorted by points (highest first).
        """

        # Create fixtures
        f1 = create_fixture(
            self.season2,
            self.division1,
            self.week1,
            self.s2_d1_team1,
            self.s2_d1_team2,
        )
        f2 = create_fixture(
            self.season2,
            self.division1,
            self.week2,
            self.s2_d1_team3,
            self.s2_d1_team1,
        )

        # Create fixture results
        # Team 1: 3pts (win + draw)
        # Team 2: 0pts (loss)
        # Team 3: 1pt (draw)
        create_fixture_result(f1, 10, 0)
        create_fixture_result(f2, 5, 5)

        response = self.client.get(reverse("tables"))
        table = response.context["division_tables"][0]["table"]

        # Teams in division 1 (current season)
        self.assertEqual(table[0]["name"], self.s2_d1_team1.team_name)
        self.assertEqual(table[0]["Pts"], 3)
        self.assertEqual(table[1]["name"], self.s2_d1_team3.team_name)
        self.assertEqual(table[1]["Pts"], 1)
        self.assertEqual(table[2]["name"], self.s2_d1_team2.team_name)
        self.assertEqual(table[2]["Pts"], 0)

    def test_context_sorts_tied_points_by_matches_then_sets(self):
        """
        Verify teams with the same points are sorted in order of
        - team matches won
        - team sets won

        Note: next tie is resolved by individual sets won but this is
        tested in a subsequent test
        """

        # Create fixtures and results to verify order by team matches then sets
        # Team 3: 2pts (win) - won 1 team match and 9 team sets
        # Team 2: 2pts (draw + draw) - won 0 team matches and 11 team sets
        # Team 1: 2pts (draw + draw) - won 0 team matches and 10 team sets
        f1 = create_fixture(
            self.season2,
            self.division1,
            self.week1,
            self.s2_d1_team1,
            self.s2_d1_team2,
        )
        f2 = create_fixture(
            self.season2,
            self.division1,
            self.week1,
            self.s2_d1_team2,
            self.s2_d1_team1,
        )
        f3 = create_fixture(
            self.season2,
            self.division1,
            self.week2,
            self.s2_d1_team3,
            self.s2_d1_team2,
        )
        create_fixture_result(f1, 5, 5)
        create_fixture_result(f2, 5, 5)
        create_fixture_result(f3, 9, 1)

        response = self.client.get(reverse("tables"))
        table = response.context["division_tables"][0]["table"]

        # Teams in division 1 (current season)
        self.assertEqual(table[0]["name"], self.s2_d1_team3.team_name)
        self.assertEqual(table[0]["Pts"], 2)
        self.assertEqual(table[0]["team_sets_won"], 9)
        self.assertEqual(table[1]["name"], self.s2_d1_team2.team_name)
        self.assertEqual(table[1]["Pts"], 2)
        self.assertEqual(table[1]["team_sets_won"], 11)
        self.assertEqual(table[2]["name"], self.s2_d1_team1.team_name)
        self.assertEqual(table[2]["Pts"], 2)
        self.assertEqual(table[2]["team_sets_won"], 10)

    def test_context_sorts_tied_team_sets_by_individual_singles_sets(self):
        """
        Verify teams with the same points, matches won and team sets won
        are sorted by individual singles sets won
        """

        # Create fixtures and results to verify order by team matches then sets
        # Team 2 (draw) - won 0 team matches, 5 team sets and 3 singles sets
        # Team 1 (draw) - won 0 team matches, 5 team sets and 2 singles sets
        f1 = create_fixture(
            self.season2,
            self.division1,
            self.week1,
            self.s2_d1_team1,
            self.s2_d1_team2,
        )
        fr1 = create_fixture_result(f1, 5, 5)
        p1 = create_player("John", "Doe", self.club)
        p2 = create_player("Joe", "Bloggs", self.club)
        tp1 = create_team_player(p1, self.s2_d1_team1)
        tp2 = create_team_player(p2, self.s2_d1_team2)
        create_singles_match(fr1, tp1, tp2, 1, 3)

        response = self.client.get(reverse("tables"))
        table = response.context["division_tables"][0]["table"]

        # Teams in division 1 (current season)
        self.assertEqual(table[0]["name"], self.s2_d1_team2.team_name)
        self.assertEqual(table[0]["Pts"], 1)
        self.assertEqual(table[0]["team_sets_won"], 5)
        self.assertEqual(table[0]["individual_sets_won"], 3)
        self.assertEqual(table[1]["name"], self.s2_d1_team1.team_name)
        self.assertEqual(table[1]["Pts"], 1)
        self.assertEqual(table[1]["team_sets_won"], 5)
        self.assertEqual(table[1]["individual_sets_won"], 1)

    def test_context_sorts_tied_team_sets_by_individual_doubles_sets(self):
        """
        Verify teams with the same points, matches won and team sets won
        are sorted by individual doubles sets won
        """

        # Create fixtures and results to verify order by team matches then sets
        # Team 2 (draw) - won 0 team matches, 5 team sets and 3 singles sets
        # Team 1 (draw) - won 0 team matches, 5 team sets and 0 singles sets
        f1 = create_fixture(
            self.season2,
            self.division1,
            self.week1,
            self.s2_d1_team1,
            self.s2_d1_team2,
        )
        fr1 = create_fixture_result(f1, 5, 5)
        p1 = create_player("Team 1", "Player 1", self.club)
        p2 = create_player("Team 1", "Player 2", self.club)
        p3 = create_player("Team 2", "Player 1", self.club)
        p4 = create_player("Team 2", "Player 2", self.club)
        tp1 = create_team_player(p1, self.s2_d1_team1)
        tp2 = create_team_player(p2, self.s2_d1_team1)
        tp3 = create_team_player(p3, self.s2_d1_team1)
        tp4 = create_team_player(p4, self.s2_d1_team1)
        create_doubles_match(fr1, [tp1, tp2], [tp3, tp4], 2, 3)

        response = self.client.get(reverse("tables"))
        table = response.context["division_tables"][0]["table"]

        # Teams in division 1 (current season)
        self.assertEqual(table[0]["name"], self.s2_d1_team2.team_name)
        self.assertEqual(table[0]["Pts"], 1)
        self.assertEqual(table[0]["team_sets_won"], 5)
        self.assertEqual(table[0]["individual_sets_won"], 3)
        self.assertEqual(table[1]["name"], self.s2_d1_team1.team_name)
        self.assertEqual(table[1]["Pts"], 1)
        self.assertEqual(table[1]["team_sets_won"], 5)
        self.assertEqual(table[1]["individual_sets_won"], 2)

    # Filters and HTMX
    def test_context_contains_form_and_filters_applied(self):
        """Verify context contains form and filters_applied."""
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn("filters_applied", response.context)

    def test_htmx_request_returns_partial_template(self):
        """Verify HTMX requests return the tables section partial."""
        response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertTemplateUsed(
            response, "league/partials/tables_section.html"
        )

    def test_htmx_season_filtering_updates_results_list(self):
        """Verify HTMX request with season filter updates the tables."""
        # Create Teams in season 1 (not current season)
        s1_d1_team1 = create_team(
            season=self.season1,
            division=self.division1,
            club=self.club,
            venue=self.venue,
            team_name="s1 d1 t1",
            home_day="monday",
            home_time=time(19, 0),
        )
        s1_d1_team2 = create_team(
            season=self.season1,
            division=self.division1,
            club=self.club,
            venue=self.venue,
            team_name="s1 d1 t2",
            home_day="monday",
            home_time=time(19, 0),
        )

        response = self.client.get(
            self.url, {"season": self.season1.slug}, HTTP_HX_REQUEST="true"
        )

        # Should contain teams from past season
        self.assertContains(response, s1_d1_team1.team_name)
        self.assertContains(response, s1_d1_team2.team_name)

        # Should not contain teams from current season
        self.assertNotContains(response, self.s2_d1_team1.team_name)
        self.assertNotContains(response, self.s2_d2_team1.team_name)


class TeamSummaryPageTests(TestCase):
    def setUp(self):

        # Create season info
        self.division = create_division(name="Division 1", rank=1)
        self.season = create_season(
            name="2024/25",
            short_name="24-25",
            slug="24-25",
            start_year=2024,
            end_year=2025,
            is_current=True,
            divisions_list=[self.division],
        )
        self.week1 = create_week(season=self.season, week_num=1)
        self.week2 = create_week(season=self.season, week_num=2)
        self.week3 = create_week(season=self.season, week_num=3)
        self.week4 = create_week(season=self.season, week_num=4)

        # Create club, venue and 3 teams
        self.club = create_club("Club 1")
        self.venue = create_venue("Venue 1")
        self.team1 = create_team(
            season=self.season,
            division=self.division,
            club=self.club,
            venue=self.venue,
            team_name="Team 1",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.team2 = create_team(
            season=self.season,
            division=self.division,
            club=self.club,
            venue=self.venue,
            team_name="Team 2",
            home_day="monday",
            home_time=time(19, 0),
        )
        self.team3 = create_team(
            season=self.season,
            division=self.division,
            club=self.club,
            venue=self.venue,
            team_name="Team 3",
            home_day="monday",
            home_time=time(19, 0),
        )

        # Create team fixtures 3 played, 1 unplayed
        self.fixture1_played_home = create_fixture(
            season=self.season,
            division=self.division,
            week=self.week1,
            home_team=self.team1,
            away_team=self.team2,
        )
        self.fixture2_played_away = create_fixture(
            season=self.season,
            division=self.division,
            week=self.week2,
            home_team=self.team3,
            away_team=self.team1,
        )
        self.fixture3_played_away = create_fixture(
            season=self.season,
            division=self.division,
            week=self.week3,
            home_team=self.team2,
            away_team=self.team1,
        )
        self.fixture4_unplayed_home = create_fixture(
            season=self.season,
            division=self.division,
            week=self.week4,
            home_team=self.team1,
            away_team=self.team3,
        )

        # Create unrelated fixture
        self.fixture_unrelated = create_fixture(
            season=self.season,
            division=self.division,
            week=self.week1,
            home_team=self.team2,
            away_team=self.team3,
        )

        # Create fixture results (a win, a draw and a loss)
        self.fixture_result1 = create_fixture_result(
            fixture=self.fixture1_played_home,
            home_score=7,
            away_score=3,
        )
        self.fixture_result2 = create_fixture_result(
            fixture=self.fixture2_played_away,
            home_score=5,
            away_score=5,
        )
        self.fixture_result3 = create_fixture_result(
            fixture=self.fixture3_played_away,
            home_score=6,
            away_score=4,
        )
        self.fixture_result_unrelated = create_fixture_result(
            fixture=self.fixture_unrelated,
            home_score=10,
            away_score=0,
        )

        self.url = reverse("team_summary", args=[self.team1.id])

    def test_team_summary_returns_200_for_valid_team(self):
        """
        Verify the view returns a 200 OK response when given a valid team ID.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_team_summary_returns_404_for_invalid_team(self):
        """
        Verify the view returns a 404 response when the team ID does not exist.
        """
        response = self.client.get(reverse("team_summary", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_team_summary_page_uses_correct_template(self):
        """Verify correct template is used for teams summary page."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "league/team_summary.html")

    # Context
    def test_context_includes_required_keys(self):
        """
        Verify that the context includes the following keys:
        - team
        - player_data
        - fixture_data
        - results_data
        - team_stats
        """
        response = self.client.get(self.url)
        self.assertIn("team", response.context)
        self.assertIn("player_data", response.context)
        self.assertIn("fixtures_data", response.context)
        self.assertIn("results_data", response.context)
        self.assertIn("team_stats", response.context)

    def test_context_team_matches_requested_team(self):
        """Verify the context variable 'team' matches the requested team."""
        response = self.client.get(self.url)
        self.assertEqual(response.context["team"], self.team1)

    def test_context_fixtures_data_order_and_contents(self):
        """
        Verify that only fixtures without results are included and that they
        are ordered in chronological order by week (earliest first).
        """
        # Delete result from 3rd fixture so have two fixtures to compare
        self.fixture_result3.delete()
        f1 = self.fixture3_played_away  # now unplayed
        f2 = self.fixture4_unplayed_home

        response = self.client.get(self.url)
        fixtures_data = response.context["fixtures_data"]
        self.assertEqual(len(fixtures_data), 2)
        self.assertEqual(fixtures_data[0]["week"], f1.week)
        self.assertEqual(fixtures_data[1]["week"], f2.week)

    def test_context_results_data_order_and_contents(self):
        """
        Verify that only results for the specified team are included in
        'results_data' and are ordered chronologically (earliest first).
        """
        response = self.client.get(self.url)
        results_data = response.context["results_data"]
        self.assertEqual(len(results_data), 3)
        self.assertEqual(results_data[0]["result"], self.fixture_result1)
        self.assertEqual(results_data[1]["result"], self.fixture_result2)
        self.assertEqual(results_data[2]["result"], self.fixture_result3)

    def test_team_stats_correctly_computed(self):
        """
        Verify that played, wins, draws, losses and points are correctly
        calculated in team_stats.
        """
        response = self.client.get(self.url)
        stats = response.context["team_stats"]
        self.assertEqual(stats["played"], 3)
        self.assertEqual(stats["wins"], 1)
        self.assertEqual(stats["draws"], 1)
        self.assertEqual(stats["losses"], 1)
        self.assertEqual(stats["points"], 3)

    def test_player_data_correctly_calculated_and_sorted(self):
        """
        Verify that player data is sorted in descending order by
        win percent then win count.
        """
        # Create players
        p1 = create_player("Player", "One", self.club)
        p2 = create_player("Player", "Two", self.club)
        p3 = create_player("Player", "Three", self.club)
        p4 = create_player("Player", "Four", self.club)
        p5 = create_player("Player", "Five", self.club)

        # Create Team Players
        t1p1 = create_team_player(p1, self.team1)
        t1p2 = create_team_player(p2, self.team1)
        t2p1 = create_team_player(p3, self.team2)
        t2p2 = create_team_player(p4, self.team2)
        t3p1 = create_team_player(p5, self.team3)

        # Create single matches
        # Team Player 1 - won 4, lost 0, 100%
        create_singles_match(self.fixture_result1, t1p1, t2p1, 3, 0)
        create_singles_match(self.fixture_result1, t1p1, t2p2, 3, 1)
        create_singles_match(self.fixture_result2, t2p1, t1p1, 0, 3)
        create_singles_match(self.fixture_result2, t2p2, t1p1, 0, 3)

        # Team Player 2 - won 2, lost 0, 100%
        create_singles_match(self.fixture_result1, t1p2, t2p1, 3, 0)
        create_singles_match(self.fixture_result1, t1p2, t2p2, 3, 0)

        # Reserve player - won 1, lost 1, 50%
        create_singles_match(self.fixture_result2, t2p1, t3p1, 3, 0)
        create_singles_match(self.fixture_result2, t2p2, t3p1, 0, 3)

        response = self.client.get(self.url)
        player_data = response.context["player_data"]

        # First item in player_data
        self.assertEqual(player_data[0]["name"], t1p1.player.full_name)
        self.assertEqual(player_data[0]["is_registered"], True)
        self.assertEqual(player_data[0]["played"], 4)
        self.assertEqual(player_data[0]["wins"], 4)
        self.assertEqual(player_data[0]["percent"], 100.0)

        # Second item in player_data
        self.assertEqual(player_data[1]["name"], t1p2.player.full_name)
        self.assertEqual(player_data[1]["is_registered"], True)
        self.assertEqual(player_data[1]["played"], 2)
        self.assertEqual(player_data[1]["wins"], 2)
        self.assertEqual(player_data[1]["percent"], 100.0)

        # Third item in player_data
        self.assertEqual(player_data[2]["name"], t3p1.player.full_name)
        self.assertEqual(player_data[2]["is_registered"], False)
        self.assertEqual(player_data[2]["played"], 2)
        self.assertEqual(player_data[2]["wins"], 1)
        self.assertEqual(player_data[2]["percent"], 50.0)
        self.assertContains(response, "(RESERVE)")

    # Placeholder fallbacks
    def test_team_with_no_fixtures_or_results_displays_placeholders(self):
        """
        Verify that a team with no fixtures or results displays the
        correct template.
        """
        # Delete all fixtures
        delete_fixtures()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["fixtures_data"], [])
        self.assertEqual(response.context["results_data"], [])
        self.assertContains(response, "No upcoming fixtures")
        self.assertContains(response, "No results to display")

    def test_team_with_all_fixtures_played_displays_placeholder(self):
        """
        Verify that a team with no remaining fixtures displays the
        correct template.
        """
        # Delete unplayed fixture
        self.fixture4_unplayed_home.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["fixtures_data"], [])
        self.assertContains(response, "No upcoming fixtures")

    def test_team_with_fixtures_but_no_results(self):
        """
        Verify a team with fixtures but no results shows correct placeholder.
        """
        # Delete fixture results but keep fixtures
        delete_fixture_results()

        response = self.client.get(self.url)
        self.assertEqual(len(response.context["fixtures_data"]), 4)
        self.assertEqual(response.context["results_data"], [])
        self.assertContains(response, "No results to display")

    def test_team_with_no_players_or_matches_handles_gracefully(self):
        """
        Verify the view handles teams with no registered players and
        no singles matches.
        """
        # Delete fixture results but keep fixtures
        delete_fixture_results()
        delete_team_players()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["player_data"], [])
        self.assertEqual(response.context["results_data"], [])
        self.assertContains(response, "No player data available")
