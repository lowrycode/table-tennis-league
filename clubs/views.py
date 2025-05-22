from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.forms.models import model_to_dict
from django.contrib import messages
from .models import Club, ClubInfo, Venue, VenueInfo, ClubVenue
from .forms import UpdateClubInfoForm, AssignClubVenueForm
from .decorators import club_admin_required


# Helper functions
def build_club_context_for_admin(club):
    # Get the latest ClubInfo (or None)
    latest_club_info = (
        ClubInfo.objects.filter(club=club).order_by("-created_on").first()
    )

    # Get all ClubVenue records for the club, including related Venue
    club_venues_qs = ClubVenue.objects.filter(club=club).select_related(
        "venue"
    )

    # Get ids for all venues used by the club as a list
    venue_ids = club_venues_qs.values_list("venue__id", flat=True)

    # Get all VenueInfo records for club venues, ordered by most recent first
    venue_infos_qs = VenueInfo.objects.filter(venue_id__in=venue_ids).order_by(
        "-created_on"
    )

    # Prefetch ClubVenues with related venue and venue infos
    club_venues = club_venues_qs.prefetch_related(
        Prefetch(
            "venue__venue_infos",
            queryset=venue_infos_qs,
            to_attr="latest_infos",
        )
    )

    # Build club_dict
    club_dict = {
        "name": club.name,
        "has_pending_info": False,
        "info": {},
        "venues": [],
    }

    # Update info
    if latest_club_info:
        club_dict["info"] = model_to_dict(latest_club_info)

    # Update venues
    for club_venue in club_venues:
        if club_venue.venue.latest_infos:
            latest_venue_info = club_venue.venue.latest_infos[0]
            venue_dict = model_to_dict(latest_venue_info)
        else:
            venue_dict = {}

        venue_dict["name"] = club_venue.venue.name
        venue_dict["id"] = club_venue.venue.id
        club_dict["venues"].append(venue_dict)

    # Update has_pending_info
    club_dict["has_pending_info"] = not club_dict["info"].get(
        "approved", True
    ) or any(not venue.get("approved", True) for venue in club_dict["venues"])

    return club_dict


# View functions
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
    club = request.user.club_admin.club
    club_dict = build_club_context_for_admin(club)

    return render(
        request,
        "clubs/admin_dashboard.html",
        {
            "club": club_dict,
        },
    )


@club_admin_required
def update_club_info(request):
    club = request.user.club_admin.club

    if request.method == "POST":
        form = UpdateClubInfoForm(request.POST, request.FILES)
        if form.is_valid():
            club_info = form.save(commit=False)
            club_info.club = club
            club_info.save()

            # Cleanup records no longer needed
            latest_approved = (
                ClubInfo.objects.filter(club=club, approved=True)
                .exclude(pk=club_info.pk)
                .order_by("-created_on")
                .first()
            )
            ClubInfo.objects.filter(club=club).exclude(
                pk__in=[club_info.pk]
                + ([latest_approved.pk] if latest_approved else [])
            ).delete()

            # Success message and redirect
            messages.success(request, "Club info has been updated.")
            return redirect("club_admin_dashboard")
        else:
            messages.warning(
                request,
                (
                    "Form data was invalid - please check the error message(s)"
                    " in the form and try again"
                ),
            )
    else:
        # Get the latest ClubInfo (or None)
        latest_club_info = (
            ClubInfo.objects.filter(club=club).order_by("-created_on").first()
        )
        if latest_club_info:
            initial_data = model_to_dict(latest_club_info)
        else:
            initial_data = {}
            initial_data["club"] = club
        form = UpdateClubInfoForm(initial=initial_data)

    return render(
        request,
        "clubs/update_club_info.html",
        {"form": form, "club": club},
    )


@club_admin_required
def delete_club_info(request):
    club = request.user.club_admin.club

    if request.method == "POST":
        data = request.POST
        option = data.get("delete_option")
        if option == "all":
            if data.get("confirm_delete") != "on":
                messages.warning(
                    request,
                    (
                        "Please tick the confirmation checkbox to confirm"
                        " that you understand the implications of this action."
                    ),
                )

            else:
                # Delete all club infos
                ClubInfo.objects.filter(club=club).delete()
                messages.success(request, "Club info has been deleted.")
                return redirect("club_admin_dashboard")

        elif option == "unapproved":
            # Delete unapproved club infos
            unapproved_club_infos = ClubInfo.objects.filter(club=club).exclude(
                approved=True
            )
            if unapproved_club_infos.count() == 0:
                messages.warning(
                    request,
                    "There is no unapproved club information to delete.",
                )
            else:
                unapproved_club_infos.delete()
                messages.success(
                    request, "Unapproved club info has been deleted."
                )
                return redirect("club_admin_dashboard")
        else:
            messages.warning(
                request,
                (
                    "An error occurred."
                    " Please contact the league administrator."
                ),
            )
    return render(request, "clubs/confirm_delete_club_info.html")


@club_admin_required
def unassign_venue(request, venue_id):
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method")

    # Get Club
    club = request.user.club_admin.club

    # Delete ClubVenue
    # This approach silently handles missing Venue or ClubVenue objects
    venue = Venue.objects.filter(id=venue_id).first()
    if venue:
        club_venue = ClubVenue.objects.filter(club=club, venue=venue).first()
        if club_venue:
            club_venue.delete()

    # Build club_dict
    club_dict = build_club_context_for_admin(club)

    return render(
        request,
        "clubs/partials/admin_club_info_section.html",
        {"club": club_dict},
    )


@club_admin_required
def assign_venue(request):
    # Get Club
    club = request.user.club_admin.club

    if request.method == "POST":
        form = AssignClubVenueForm(request.POST, club=club)
        if form.is_valid():
            # Assign venue
            club_venue = form.save(commit=False)
            club_venue.club = club
            club_venue.save()

            # Message and redirect
            messages.success(request, "Venue has been assigned.")
            return redirect("club_admin_dashboard")
        else:
            messages.warning(
                request,
                "Something went wrong."
                " Please check that the venue is not already assigned.",
            )
    else:
        form = AssignClubVenueForm(club=club)

    no_available_venues = not form.fields["venue"].queryset.exists()

    return render(
        request,
        "clubs/assign_venue.html",
        {"form": form, "no_available_venues": no_available_venues},
    )
