from django.db.models import Prefetch
from django.shortcuts import render
from .models import Club, ClubInfo


def clubs(request):
    all_clubs = Club.objects.prefetch_related(
        Prefetch(
            "infos",
            queryset=ClubInfo.objects.filter(approved=True).order_by(
                "-created_on"
            ),
            to_attr="approved_infos",
        )
    )
    clubs = []
    for club in all_clubs:
        if club.approved_infos:
            data = club.approved_infos[0]
            data.name = club.name
            clubs.append(data)
    return render(request, "clubs/clubs.html", {"clubs": clubs})
