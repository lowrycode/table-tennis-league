from django.utils import timezone
from django.db import models


# Create your models here.
class NewsItem(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    active_from = models.DateTimeField(default=timezone.now)
    active_to = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-active_from', 'title']

    def __str__(self):
        return self.title
