from django.db import models


# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rank = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["rank"]

    def __str__(self):
        return self.name
