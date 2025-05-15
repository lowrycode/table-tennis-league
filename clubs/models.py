from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ClubInfo(models.Model):
    club = models.OneToOneField(
        Club, on_delete=models.CASCADE, related_name="info"
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
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.club.name

    def clean(self):
        super().clean()
        if len(self.description) > 500:
            raise ValidationError(
                {
                    "description": "Cannot be more than 500 characters."
                }
            )
        if len(self.session_info) > 500:
            raise ValidationError(
                {
                    "session_info": "Cannot be more than 500 characters."
                }
            )
