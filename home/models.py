from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


# Create your models here.
class NewsItem(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    active_from = models.DateTimeField(default=timezone.now)
    active_to = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-active_from", "title"]

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        return self.active_from <= now and (
            self.active_to is None or self.active_to >= now
        )

    def clean(self):
        super().clean()
        # Check active_to is later than active_from
        if self.active_to and self.active_from >= self.active_to:
            raise ValidationError(
                '"Active from" date must be earlier than "Active to" date.'
            )
        # Check active_to is in future
        now = timezone.now()
        if self.active_to and self.active_to <= now:
            raise ValidationError('"Active to" date must be in the future.')
