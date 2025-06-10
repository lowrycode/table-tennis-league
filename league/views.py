from django.shortcuts import render
from .models import Season, Week


def fixtures(request):
    season = (
        Season.objects.filter(is_current=True).order_by("-start_date").first()
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

    # Used for the fixture status colour key (format: CSS class, label)
    fixture_status_key = [
        ("fixture-scheduled", "Scheduled"),
        ("fixture-completed", "Completed"),
        ("fixture-postponed", "Postponed"),
        ("fixture-cancelled", "Cancelled"),
    ]

    return render(
        request,
        "league/fixtures.html",
        {
            "season": season,
            "weeks": weeks,
            "fixture_status_key": fixture_status_key,
        },
    )
