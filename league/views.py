from django.shortcuts import render
from .models import Season, Week


def fixtures(request):
    season = (
        Season.objects.filter(is_current=True)
        .order_by("-start_date")
        .first()
    )
    if not season:
        return render(
            request, "league/fixtures.html", {"season": None, "weeks": None}
        )

    weeks = (
        Week.objects.filter(season=season)
        .prefetch_related(
            "week_fixtures__home_team",
            "week_fixtures__away_team",
            "week_fixtures__venue",
        )
        .order_by("start_date")
    )

    return render(
        request, "league/fixtures.html", {"season": season, "weeks": weeks}
    )
