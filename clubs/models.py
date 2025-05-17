from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ClubInfo(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="club_infos"
    )
    website = models.URLField(null=True, blank=True)
    image = CloudinaryField("image", default="placeholder")
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField(null=True, blank=True)
    description = models.TextField()
    session_info = models.TextField()
    beginners = models.BooleanField(default=False)
    intermediates = models.BooleanField(default=False)
    advanced = models.BooleanField(default=False)
    kids = models.BooleanField(default=False)
    adults = models.BooleanField(default=False)
    coaching = models.BooleanField(default=False)
    league = models.BooleanField(default=False)
    equipment_provided = models.BooleanField(default=False)
    membership_required = models.BooleanField(default=False)
    free_taster = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Club Information"
        ordering = ["club", "-created_on"]

    def __str__(self):
        created_on_str = (
            self.created_on.strftime("%d/%m/%y at %I:%M %p")
            if self.created_on
            else "No date"
        )
        return f"{self.club.name} ({created_on_str})"

    def clean(self):
        super().clean()
        if len(self.description) > 500:
            raise ValidationError(
                {"description": "Cannot be more than 500 characters."}
            )
        if len(self.session_info) > 500:
            raise ValidationError(
                {"session_info": "Cannot be more than 500 characters."}
            )


class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class VenueInfo(models.Model):
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="venue_infos"
    )
    street_address = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    num_tables = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    parking_info = models.TextField(max_length=500)
    meets_league_standards = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        created_on_str = (
            self.created_on.strftime("%d/%m/%y at %I:%M %p")
            if self.created_on
            else "No date"
        )
        return f"{self.venue} ({created_on_str})"

    def clean(self):
        super().clean()
        if len(self.parking_info) > 500:
            raise ValidationError(
                {"description": "Cannot be more than 500 characters."}
            )


class ClubVenue(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="club_venues"
    )
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="venue_clubs"
    )

    class Meta:
        unique_together = ("club", "venue")
        ordering = ["club", "venue"]

    def __str__(self):
        return f"{self.club.name} at {self.venue.name}"
