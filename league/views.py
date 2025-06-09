from django.shortcuts import render, get_object_or_404
from .models import Season, Week


def fixtures(request):
    season = get_object_or_404(Season, is_current=True)
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
