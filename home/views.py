from django.shortcuts import render
from .models import NewsItem
from django.utils import timezone
from django.db import models


def home(request):
    """
    Render the home page with news items that are currently active.
    """
    now = timezone.now()
    active_news_items = NewsItem.objects.filter(active_from__lte=now).filter(
        models.Q(active_to__isnull=True) | models.Q(active_to__gte=now)
    )
    return render(
        request, "home/home.html", {"active_news_items": active_news_items}
    )
