from datetime import time, timedelta
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError
from clubs.models import Club, Venue
from .validators import validate_match_time


class Division(models.Model):
    """
    Represents a competitive division, ordered by rank.
    Divisions are shared across multiple seasons.
    """

    name = models.CharField(max_length=50, unique=True)
    rank = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["rank"]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Prevent deletion if the division is linked to any seasons
        if self.seasons.exists():
            raise ValidationError(
                "This division cannot be deleted because it is linked "
                "to season data."
            )
        super().delete(*args, **kwargs)


class Season(models.Model):
    """
    Represents a single season in the league.
    """

    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    divisions = models.ManyToManyField(Division, related_name="seasons")
    start_date = models.DateField()
    end_date = models.DateField()
    registration_opens = models.DateTimeField()
    registration_closes = models.DateTimeField()
    is_visible = models.BooleanField(default=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        # Enforce divisions as a required field
        if self.pk and self.divisions.count() == 0:
            raise ValidationError(
                {"divisions": "At least one division is required."}
            )

        # Enforce start date must be earlier than end date
        if (
            self.start_date
            and self.end_date
            and self.start_date >= self.end_date
        ):
            raise ValidationError(
                {"start_date": "Start date must be earlier than end date."}
            )

        # Enforce registration_opens must be earlier than registration_closes
        if (
            self.registration_opens
            and self.registration_closes
            and self.registration_opens >= self.registration_closes
        ):
            raise ValidationError(
                {
                    "registration_opens": (
                        "Registration opens must be before "
                        "registration closes."
                    )
                }
            )

        # Enforce registration_closes must be before start_date
        if (
            self.registration_closes
            and self.start_date
            and self.registration_closes.date() >= self.start_date
        ):
            raise ValidationError(
                {
                    "registration_closes": (
                        "Registration closes must be before "
                        "the season start date."
                    )
                }
            )

    def save(self, *args, **kwargs):
        if self.is_current:
            # Unset is_current on all other seasons
            Season.objects.filter(is_current=True).exclude(pk=self.pk).update(
                is_current=False
            )
        super().save(*args, **kwargs)


class Week(models.Model):
    """
    Represents a named week within a season.

    Used to group fixtures by date.
    """

    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="season_weeks"
    )
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()

    class Meta:
        ordering = ["start_date"]
        # Ensure week names are unique within a season
        constraints = [
            models.UniqueConstraint(
                fields=["season", "name"], name="unique_season_and_name"
            )
        ]

    def __str__(self):
        return self.name


class Player(models.Model):
    """
    Represents an individual player, optionally linked to a club.

    Uniqueness is enforced by name and date of birth.
    """

    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("pending", "Pending"),
        ("rejected", "Rejected"),
    ]

    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    current_club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="club_players",
    )
    club_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )

    class Meta:
        ordering = ["surname", "forename"]
        constraints = [
            models.UniqueConstraint(
                fields=["forename", "surname", "date_of_birth"],
                name="unique_forename_surname_dob",
            )
        ]

    def __str__(self):
        return (
            f"{self.surname}, {self.forename} "
            f"({self.date_of_birth.strftime('%d %b %Y')})"
        )

    @property
    def full_name(self):
        return f"{self.forename} {self.surname}"

    def save(self, *args, **kwargs):
        # Using title rather than capitalize so works on multi-word names
        self.forename = self.forename.title()
        self.surname = self.surname.title()
        super().save(*args, **kwargs)


class Team(models.Model):
    """
    Represents a club team competing in a division during a season.

    Includes default details for home venue, match day and match time.
    """

    DAY_CHOICES = [
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
    ]

    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="season_teams",
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.PROTECT,
        related_name="division_teams",
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name="club_teams",
    )
    home_venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name="venue_teams",
    )
    team_name = models.CharField(max_length=30)
    home_day = models.CharField(
        max_length=10,
        choices=DAY_CHOICES,
        default="monday",
        verbose_name="Home match day",
    )
    home_time = models.TimeField(
        validators=[validate_match_time],
        default=time(19, 0),
        verbose_name="Home match start time",
    )
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["team_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["team_name", "season"],
                name="team_name_and_season",
            )
        ]

    def __str__(self):
        return f"{self.team_name} ({self.season.short_name})"

    def save(self, *args, **kwargs):
        """Ensure team_name has title case"""
        self.team_name = self.team_name.title()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # Prevent changing division after season start date
        if self.pk:
            existing = Team.objects.get(pk=self.pk)
            if (
                existing.division != self.division
                and self.season.start_date <= now().date()
            ):
                raise ValidationError(
                    {
                        "division": (
                            "Division cannot be changed after the "
                            "season has started."
                        )
                    }
                )


class TeamPlayer(models.Model):
    """
    Links a player to a team for a given season.

    Enforces eligibility and club association constraints.
    """

    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name="player_teams",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="team_players",
    )
    paid_fees = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Team players"
        ordering = ["player__surname", "player__forename"]

    def __str__(self):
        return f"{self.player.full_name} ({self.team.team_name})"

    def clean(self):
        """
        Ensures the player has a confirmed club association
        and that it matches the club related to the team in
        this TeamPlayer record.
        """
        super().clean()

        # Ensure the player has confirmed club status
        if self.player.club_status != "confirmed":
            raise ValidationError(
                "Club Admin must confirm that the player is associated "
                "with their club before proceeding."
            )

        # Ensure the player's club matches the club in the team for
        # this TeamPlayer's club
        if self.player.current_club != self.team.club:
            raise ValidationError(
                "The player's profile states that they are not associated "
                "with the team club."
            )

        # Ensure player not already registered to another team in this season
        season = self.team.season
        existing = TeamPlayer.objects.filter(
            player=self.player, team__season=season
        ).exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError(
                f"{self.player} is already registered with another team "
                f"in {season}."
            )


class Fixture(models.Model):
    """
    Represents a scheduled match between two teams in a season.
    Includes timing, venue and match status.
    """

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("postponed", "Postponed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="season_fixtures",
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.PROTECT,
        related_name="division_fixtures",
    )
    week = models.ForeignKey(
        Week,
        on_delete=models.PROTECT,
        related_name="week_fixtures",
    )
    datetime = models.DateTimeField()
    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="home_fixtures",
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="away_fixtures",
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        related_name="venue_fixtures",
        null=True,
        blank=True,
        help_text="Leave blank to auto-assign the home team's venue",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="scheduled"
    )

    class Meta:
        ordering = ["datetime"]
        constraints = [
            models.UniqueConstraint(
                fields=["season", "home_team", "away_team"],
                name="season_with_home_and_away_team_unique",
            )
        ]

    def __str__(self):
        return (
            f"{self.season.short_name} {self.week.name} - "
            f"{self.home_team.team_name} vs {self.away_team.team_name}"
        )

    def clean(self):
        """
        Enforce custom constraints.

        These include
        1. home team must be different to away team
        2. both teams must be in the specified division
        3. both teams must be in the specified season
        """
        super().clean()

        # Validate time part of datetime - must be between 6pm and 8pm
        if self.datetime:
            match_time = self.datetime.time()
            validate_match_time(match_time)

        # Validate date part of datetime
        # must be within 6 days of week.start_date
        if self.datetime and self.week:
            start = self.week.start_date
            end = start + timedelta(days=6)
            if not (start <= self.datetime.date() <= end):
                raise ValidationError(
                    {
                        "datetime": (
                            "Date must be within the same week "
                            f"({start} to {end})."
                        )
                    }
                )

        # Enforce home team and away team are different
        if self.home_team_id and self.away_team_id:
            if self.home_team == self.away_team:
                raise ValidationError("A team cannot play against itself.")

        # Enforce division
        if self.home_team_id and self.division:
            if self.home_team.division != self.division:
                raise ValidationError(
                    {"home_team": "Home team is not in the selected division."}
                )

        if self.away_team_id and self.division:
            if self.away_team.division != self.division:
                raise ValidationError(
                    {"away_team": "Away team is not in the selected division."}
                )

        # Enforce season
        if self.home_team_id and self.season:
            if self.home_team.season != self.season:
                raise ValidationError(
                    {"home_team": "Home team is not in the selected season."}
                )

        if self.away_team_id and self.season:
            if self.away_team.season != self.season:
                raise ValidationError(
                    {"away_team": "Away team is not in the selected season."}
                )

    def save(self, *args, **kwargs):
        # Auto-assign venue if blank using home team's default home_venue
        if not self.venue and self.home_team:
            self.venue = self.home_team.home_venue

        super().save(*args, **kwargs)
