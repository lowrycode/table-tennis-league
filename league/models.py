from django.db import models
from django.core.exceptions import ValidationError


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
