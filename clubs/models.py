from django.db import models
from cloudinary.models import CloudinaryField


class ClubInfo(models.Model):
    image = CloudinaryField('image', default='placeholder')
