from django.db import models
from cloudinary.models import CloudinaryField


class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ClubInfo(models.Model):
    image = CloudinaryField('image', default='placeholder')
