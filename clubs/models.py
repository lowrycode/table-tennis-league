from django.db import models
from cloudinary.models import CloudinaryField


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

    def __str__(self):
        return self.club.name
