from django.urls import reverse
from django.db import transaction
from django.db.models import Prefetch, Avg, Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponseForbidden,
    HttpResponse,
    HttpResponseBadRequest,
)
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Club, ClubInfo, Venue, VenueInfo, ClubVenue, ClubReview
from .forms import (
    UpdateClubInfoForm,
    AssignClubVenueForm,
    UpdateVenueInfoForm,
    CreateVenueForm,
    ClubReviewForm,
)
from .decorators import club_admin_required
from .filters import ClubInfoFilter


# Helper functions
def build_club_context_for_admin(club):
    """
    Builds a dictionary representing the latest state of a club for admin use.

    Includes
    - the most recent ClubInfo (approved or not)
    - a list of associated venues with their latest VenueInfo
    - a flag indicating if there is any unapproved club or venue information.

    Args:
        club (Club): The club for which to build the context variable.

    Returns:
        dict: A dictionary containing club details, venue info, and approval
        status to be passed to the template.
    """
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
        "id": club.id,
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


def build_locations_context(approved_venue_infos_qs, approved_club_infos_qs):
    """
    Builds a list of location dictionaries for venues associated with clubs
    that have at least one approved ClubInfo entry.

    Each location dictionary contains venue details and a list of clubs linked
    to that venue. This information is presented on the website when a user
    clicks on a Google Map marker.

    Args:
        approved_venue_infos_qs (QuerySet): QuerySet of approved VenueInfo
            objects ordered by most recent.
        approved_club_infos_qs (QuerySet): QuerySet of approved ClubInfo
            objects used to determine which clubs have approved info.

    Returns:
        list of dict: A list of location dictionaries.
    """
    approved_club_ids = set(
        approved_club_infos_qs.values_list("club_id", flat=True)
    )

    venue_infos = approved_venue_infos_qs.select_related(
        "venue"
    ).prefetch_related("venue__venue_clubs__club")

    locations = []
    seen_venues = set()

    for vi in venue_infos:
        # Skip if missing venue coordinates (so map won't break)
        if vi.latitude is None or vi.longitude is None:
            continue

        # Skip outdated versions
        venue_id = vi.venue.id
        if venue_id in seen_venues:
            continue
        seen_venues.add(venue_id)

        # Get clubs with approved club infos
        clubs = [
            {"id": cv.club.id, "name": cv.club.name}
            for cv in vi.venue.venue_clubs.all()
            if cv.club.id in approved_club_ids
        ]

        # Skip if no approved clubs
        if not clubs:
            continue

        # Add dictionary to locations list
        locations.append(
            {
                "name": vi.venue.name,
                "address": f"{vi.street_address}, {vi.city}, {vi.postcode}",
                "lat": vi.latitude,
                "lng": vi.longitude,
                "clubs": clubs,
            }
        )

    return locations


# View functions
def clubs(request):
    """
    Renders a public-facing list of all clubs with approved information.

    Filters ClubInfo records based on GET parameters, then attaches approved
    ClubInfo and VenueInfo to each club for display.

    Displays only clubs that have approved club information.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with clubs and filters.
    """
    # Get all approved ClubInfo records (ordered by most recent)
    approved_club_infos_qs = ClubInfo.objects.filter(approved=True).order_by(
        "-created_on"
    )

    # Filter approved ClubInfos
    club_info_filter = ClubInfoFilter(
        request.GET, queryset=approved_club_infos_qs
    )
    filtered_club_infos_qs = club_info_filter.qs

    # Prefetch filtered approved ClubInfos
    # to make accessible via club.approved_club_infos
    approved_club_infos_pf = Prefetch(
        "club_infos",
        queryset=filtered_club_infos_qs,
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

    # Get all Clubs with annotated review data and prefetch approved
    # ClubInfos and ClubVenues
    all_clubs = (
        Club.objects.annotate(
            review_average_score=Avg(
                "reviews__score", filter=Q(reviews__approved=True)
            ),
            review_count=Count("reviews", filter=Q(reviews__approved=True)),
        )
        .prefetch_related(approved_club_infos_pf, approved_venue_infos_pf)
        .order_by("name")
    )

    # Build clubs list for passing to template
    clubs_list = []
    for club in all_clubs:
        # Build club_dict
        club_dict = {
            "id": club.id,
            "name": club.name,
            "info": {},
            "venues": [],
            "review_average_score": (
                round(club.review_average_score, 1)
                if club.review_average_score
                else None
            ),
            "review_average_score_int": (
                int(club.review_average_score + 0.5)
                if club.review_average_score
                else None
            ),
            "review_count": club.review_count,
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
            clubs_list.append(club_dict)

    # Build locations_list for passing to template
    locations_list = build_locations_context(
        approved_venue_infos_qs, approved_club_infos_qs
    )

    # Deduce whether filters are applied by checking for get parameters
    filters_applied = len(request.GET) > 0

    context = {
        "clubs": clubs_list,
        "filter": club_info_filter,
        "filters_applied": filters_applied,
        "locations": locations_list,
    }

    # If htmx request, return only the club info partial template
    if request.headers.get("HX-Request") == "true":
        return render(
            request, "clubs/partials/club_info_section.html", context
        )

    return render(request, "clubs/clubs.html", context)


def club_reviews(request, club_id):
    """
    Display reviews for a specific club.

    Retrieves the club by ID and gathers all associated reviews.
    If the user is authenticated, their own review (if it exists) is
    separated from the rest. Only approved reviews are included
    in the average score and review count calculations.

    Args:
        request (HttpRequest): The HTTP request object.
        club_id (int): The primary key of the club.

    Returns:
        HttpResponse: Rendered HTML page with review details for the club.
    """

    club = get_object_or_404(Club, id=club_id)

    # Query sets
    all_club_reviews = ClubReview.objects.filter(club=club)
    approved_club_reviews = all_club_reviews.filter(approved=True)

    # Get review count and average score
    aggregate_data = approved_club_reviews.aggregate(
        avg_score=Avg("score"), count=Count("id")
    )
    review_count = aggregate_data["count"]
    average_score = aggregate_data["avg_score"]

    # Round average_score to 1 decimal place and get average_score_int
    average_score_int = None
    if average_score:
        average_score_int = int(average_score + 0.5)  # for standard rounding
        average_score = round(average_score, 1)

    # Get reviews
    if request.user.is_authenticated:
        # Seperate user's own review from other reviews
        user_review = all_club_reviews.filter(user=request.user).first()
        club_reviews = approved_club_reviews.exclude(user=request.user)
    else:
        user_review = None
        club_reviews = approved_club_reviews

    return render(
        request,
        "clubs/club_reviews.html",
        {
            "club": club,
            "user_review": user_review,
            "other_reviews": club_reviews,
            "average_score_int": average_score_int,
            "average_score": average_score,
            "review_count": review_count,
        },
    )


def venue_modal(request, venue_id):
    """
    Handles HTMX request for venue information modal.

    Returns a rendered HTML partial if the venue and approved info exist.
    Otherwise, returns an informative message.
    """
    # If not HTMX request, return error 400
    if not request.headers.get("HX-Request") == "true":
        return HttpResponseBadRequest(
            "This endpoint is for HTMX requests only."
        )

    # Get venue
    venue = Venue.objects.filter(id=venue_id).first()

    # If venue not found
    if not venue:
        return HttpResponse('<p class="mt-2 fw-semibold">Venue not found</p>')

    # Get latest approved venue info
    latest_venue_info = (
        VenueInfo.objects.filter(venue=venue, approved=True)
        .order_by("-created_on")
        .first()
    )

    # If no approved venue info found
    if not latest_venue_info:
        return HttpResponse(
            '<p class="mt-2 fw-semibold">No venue info available</p>'
        )

    # Build venue_dict
    venue_dict = model_to_dict(latest_venue_info)
    venue_dict["name"] = venue.name
    venue_dict["id"] = venue.id

    return render(
        request, "clubs/partials/club_venue.html", {"venue": venue_dict}
    )


# Views restricted to logged-in users
@login_required
def create_club_review(request, club_id):
    """
    Renders a page with a form for creating a club review.

    The view is restricted to authenticated users who have not already written
    a review for the club.

    Args:
        request (HttpRequest): The HTTP request object.
        club_id (int): The primary key of the club.

    Returns:
        HttpResponse: Rendered HTML page with review details for the club.
    """

    club = get_object_or_404(Club, id=club_id)

    # Check user has not already written a review for this club
    existing_review = ClubReview.objects.filter(
        club=club, user=request.user
    ).first()
    if existing_review:
        messages.warning(
            request,
            "You have already written a review for this club.",
        )
        return redirect(reverse("club_reviews", args=[club.id]))

    if request.method == "POST":
        club_review_form = ClubReviewForm(request.POST)
        if club_review_form.is_valid():
            club_review = club_review_form.save(commit=False)
            club_review.club = club
            club_review.user = request.user
            club_review.save()

            # Success message and redirect
            messages.success(
                request,
                (
                    f"Your review for {club.name} has been created "
                    "and is awaiting approval."
                ),
            )
            return redirect(reverse("club_reviews", args=[club.id]))
    else:
        club_review_form = ClubReviewForm()

    return render(
        request,
        "clubs/create_club_review.html",
        {
            "club": club,
            "form": club_review_form,
        },
    )


# Views restricted to Club Admins
@club_admin_required
def club_admin_dashboard(request):
    """
    Renders the admin dashboard for a club administrator.

    Displays current club and venue information alongside its status
    (approved or pending approval).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered admin dashboard for the user's assigned club.
    """
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
    """
    Allows a club admin to update club information by adding a new record.

    If submitted and valid, the new club information record is created,
    the latest approved record is kept for reference (or retrieval)
    and other outdated records are removed.

    The form is pre-filled with the most recent club information (if exists).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered Update Club Info page with form
        or redirect to dashboard after successful update.
    """
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
    """
    Allows a club admin to delete club information records.

    Admins can choose to:
    - Delete all club info records (with confirmation checkbox).
    - Delete only unapproved records.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the dashboard on successful deletion,
        or renders a confirmation page with messages.
    """
    club = request.user.club_admin.club

    if request.method == "POST":
        data = request.POST
        option = data.get("delete_option")
        if option == "all":
            if data.get("confirm_action") != "on":
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
    """
    Allows a club admin to unassign a venue from the club admin page.

    Only accepts POST requests. Silently ignores missing venue or assignment.

    Args:
        request (HttpRequest): The HTTP request object.
        venue_id (int): The ID of the venue to unassign.

    Returns:
        HttpResponse: Renders updated club info section as partial HTML.
    """
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
    """
    Allows a club admin to assign an available venue to their club.

    Handles form validation and prevents duplicate assignments.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders Assign Venue page with form or redirects to
        the dashboard on success.
    """
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


@club_admin_required
def update_venue_info(request, venue_id):
    """
    Allows a club admin to update venue information for venues linked to
    their club by adding a new record.

    Shared venues (used by multiple clubs) are indicated but still editable.
    Only the latest and one approved VenueInfo record is kept - any outdated
    records are deleted.

    Args:
        request (HttpRequest): The HTTP request object.
        venue_id (int): The ID of the venue to update.

    Returns:
        HttpResponse: Renders the Update Venue page with form or redirects
        to the dashboard on success.
    """
    # Get club
    club = request.user.club_admin.club

    # Ensure venue is assigned to this club
    try:
        club_venue = ClubVenue.objects.get(club=club, venue__id=venue_id)
        venue = club_venue.venue
    except ClubVenue.DoesNotExist:
        messages.warning(request, "Unable to edit venue information.")
        return redirect("club_admin_dashboard")

    # Check if venue is shared
    club_venues_count = ClubVenue.objects.filter(venue=venue).count()
    is_shared_venue = True if club_venues_count > 1 else False

    if request.method == "POST":
        form = UpdateVenueInfoForm(request.POST)
        if form.is_valid():
            venue_info = form.save(commit=False)
            venue_info.venue = venue
            venue_info.save()

            # Cleanup records no longer needed
            latest_approved = (
                VenueInfo.objects.filter(venue=venue, approved=True)
                .exclude(pk=venue_info.pk)
                .order_by("-created_on")
                .first()
            )
            VenueInfo.objects.filter(venue=venue).exclude(
                pk__in=[venue_info.pk]
                + ([latest_approved.pk] if latest_approved else [])
            ).delete()

            # Success message and redirect
            messages.success(request, "Venue info has been updated.")
            return redirect("club_admin_dashboard")
        else:
            messages.warning(
                request,
                ("Please correct the highlighted errors below and try again."),
            )
    else:
        # Get the latest venueInfo (or None)
        latest_venue_info = (
            VenueInfo.objects.filter(venue=venue)
            .order_by("-created_on")
            .first()
        )
        if latest_venue_info:
            initial_data = model_to_dict(latest_venue_info)
        else:
            initial_data = {}
        form = UpdateVenueInfoForm(initial=initial_data)

    return render(
        request,
        "clubs/update_venue_info.html",
        {"venue": venue, "form": form, "is_shared_venue": is_shared_venue},
    )


@club_admin_required
def create_venue(request):
    """
    Allows a club admin to create a new venue along with its initial
    VenueInfo record.

    Both venue and its info must pass validation. Uses atomic transaction.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders Create Venue page with forms or redirects
        to dashboard on success.
    """
    if request.method == "POST":
        venue_form = CreateVenueForm(request.POST)
        venue_info_form = UpdateVenueInfoForm(request.POST)
        if venue_form.is_valid() and venue_info_form.is_valid():
            # Create venue and venue_info record
            with transaction.atomic():
                venue = venue_form.save()
                venue_info = venue_info_form.save(commit=False)
                venue_info.venue = venue
                venue_info.save()

            # Success message and redirect
            messages.success(
                request,
                "Venue has been created and can now be assigned to a club.",
            )
            return redirect("club_admin_dashboard")
    else:
        venue_form = CreateVenueForm()
        venue_info_form = UpdateVenueInfoForm()

    return render(
        request,
        "clubs/create_venue.html",
        {
            "venue_form": venue_form,
            "venue_info_form": venue_info_form,
        },
    )


@club_admin_required
def delete_venue(request, venue_id):
    """
    Allows a club admin to delete a venue or unapproved venue info records.

    Deletes the entire venue only if it is not shared and the admin confirms.
    Alternatively, can delete only unapproved venue info records.

    Args:
        request (HttpRequest): The HTTP request object.
        venue_id (int): The ID of the venue to delete.

    Returns:
        HttpResponse: Renders the Confirm Venue Deletion page or redirects
        to the dashboard on success.
    """
    # Get Club and Venue
    club = request.user.club_admin.club
    venue = Venue.objects.filter(id=venue_id).first()

    # Exit early if venue doesn't exist
    if not venue:
        # Redirect to club admin page with warning message
        messages.warning(request, ("Unable to delete venue."))
        return redirect("club_admin_dashboard")

    # Exit early if venue not currently assigned to this club
    if not ClubVenue.objects.filter(venue=venue, club=club).exists():
        messages.warning(request, "Unable to delete venue.")
        return redirect("club_admin_dashboard")

    # Assign is_shared_venue context variable
    is_shared_venue = (
        ClubVenue.objects.filter(venue=venue).exclude(club=club).exists()
    )

    # Process delete request
    if request.method == "POST":
        data = request.POST
        option = data.get("delete_option")
        if option == "all":
            if is_shared_venue:
                messages.warning(
                    request,
                    (
                        "Cannot delete venue because it is shared with"
                        " at least one other club."
                    ),
                )
            elif data.get("confirm_action") != "on":
                messages.warning(
                    request,
                    (
                        "Please tick the confirmation checkbox to confirm"
                        " that you understand the implications of this action."
                    ),
                )
            else:
                # Delete venue
                Venue.objects.filter(id=venue.id).delete()
                messages.success(request, "Venue has been deleted.")
                return redirect("club_admin_dashboard")

        elif option == "unapproved":
            # Delete unapproved venue infos
            unapproved_venue_infos = VenueInfo.objects.filter(
                venue=venue
            ).exclude(approved=True)
            if unapproved_venue_infos.count() == 0:
                messages.warning(
                    request,
                    "There is no unapproved venue information to delete.",
                )
            else:
                unapproved_venue_infos.delete()
                messages.success(
                    request, "Unapproved venue info has been deleted."
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

    return render(
        request,
        "clubs/confirm_delete_venue.html",
        {"venue": venue, "is_shared_venue": is_shared_venue},
    )
