from django.db.models import Prefetch
from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import Club, ClubInfo, VenueInfo, ClubVenue
from .decorators import club_admin_required


def clubs(request):
    # Get all approved ClubInfo records (ordered by most recent)
    approved_club_infos_qs = ClubInfo.objects.filter(approved=True).order_by(
        "-created_on"
    )

    # Prefetch approved ClubInfos
    # to make accessible via club.approved_club_infos
    approved_club_infos_pf = Prefetch(
        "club_infos",
        queryset=approved_club_infos_qs,
        to_attr="approved_club_infos",
    )

    # Get all approved VenueInfo records (ordered by most recent)
    approved_venue_infos_qs = VenueInfo.objects.filter(approved=True).order_by(
        "-created_on"
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
    clubs_dict = []
    for club in all_clubs:
        # Build club_dict
        club_dict = {
            "name": club.name,
            "info": {},
            "venues": [],
        }

        if club.approved_club_infos:
            # Update club info
            latest_approved_club_info = club.approved_club_infos[0]
            club_dict["info"] = model_to_dict(latest_approved_club_info)

            # Update club venues
            for club_venue in club.approved_club_venues:
                venue = club_venue.venue
                if venue.approved_venue_infos:
                    # Attach most recently approved VenueInfo
                    latest_venue_info = venue.approved_venue_infos[0]
                    venue_dict = model_to_dict(latest_venue_info)
                    venue_dict["name"] = venue.name
                    club_dict["venues"].append(venue_dict)

            # Append club data
            clubs_dict.append(club_dict)

    return render(request, "clubs/clubs.html", {"clubs": clubs_dict})


@club_admin_required
def club_admin_dashboard(request):
    return render(request, "clubs/admin_dashboard.html")
