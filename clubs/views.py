from django.db.models import Prefetch
from django.shortcuts import render
from .models import Club, ClubInfo, VenueInfo, ClubVenue
from .decorators import club_admin_required


def clubs(request):
    # Define queryset for approved ClubInfos (ordered by most recent)
    approved_club_infos_qs = ClubInfo.objects.filter(approved=True).order_by(
        "-created_on"
    )

    # Define queryset for approved VenueInfos (ordered by most recent)
    approved_venue_infos_qs = VenueInfo.objects.filter(approved=True).order_by(
        "-created_on"
    )

    # Prefetch approved ClubInfos
    # to make accessible via club.approved_club_infos
    approved_club_infos_pf = Prefetch(
        "club_infos",
        queryset=approved_club_infos_qs,
        to_attr="approved_club_infos",
    )

    # Prefetch ClubVenues with approved VenueInfos (via ClubVenue)
    # to make accessible via club.approved_club_venues
    approved_venue_infos_pf = Prefetch(
        "club_venues",
        queryset=ClubVenue.objects.select_related("venue").prefetch_related(
            Prefetch(
                "venue__venue_infos",
                queryset=approved_venue_infos_qs,
                to_attr="approved_venue_infos",
            )
        ),
        to_attr="approved_club_venues",
    )

    # Get all Clubs and attach approved ClubInfos and ClubVenues
    all_clubs = Club.objects.prefetch_related(
        approved_club_infos_pf, approved_venue_infos_pf
    )

    # Build clubs dictionary for passing to template
    clubs = []
    for club in all_clubs:
        if club.approved_club_infos:
            club_info = club.approved_club_infos[0]
            club_info.name = club.name

            # Filter venues that have at least one approved VenueInfo
            venues = []
            for club_venue in club.approved_club_venues:
                venue = club_venue.venue
                if (
                    hasattr(venue, "approved_venue_infos")
                    and venue.approved_venue_infos
                ):
                    # Attach most recently approved VenueInfo
                    venue_info = venue.approved_venue_infos[0]
                    venue_info.name = venue.name
                    venues.append(venue_info)

            club_info.venues = venues
            clubs.append(club_info)

    return render(request, "clubs/clubs.html", {"clubs": clubs})


@club_admin_required
def club_admin_dashboard(request):
    return render(request, "clubs/admin_dashboard.html")
