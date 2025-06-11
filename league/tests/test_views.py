from datetime import time
from django.test import TestCase
from django.urls import reverse
from test_utils.helpers import (
    create_club,
    create_division,
    create_fixture,
    create_season,
    create_team,
    create_venue,
    create_week,
    delete_fixtures,
    delete_weeks,
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
