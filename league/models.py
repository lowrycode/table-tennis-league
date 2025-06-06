from datetime import time
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError
from clubs.models import Club, Venue
from .validators import validate_match_time


class Division(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rank = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["rank"]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.seasons.exists():
            raise ValidationError(
                "This division cannot be deleted because it is linked "
                "to season data."
            )
        super().delete(*args, **kwargs)


class Season(models.Model):
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
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="season_weeks"
    )
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()

    class Meta:
        ordering = ["start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["season", "name"], name="unique_season_and_name"
            )
        ]

    def __str__(self):
        return self.name

    # def delete(self, *args, **kwargs):
    #     if self.week_fixtures.exists():
    #         raise ValidationError(
    #             "This division cannot be deleted because it is linked "
    #             "to season data."
    #         )
    #     super().delete(*args, **kwargs)


class Player(models.Model):
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
