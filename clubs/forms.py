"""
Forms for managing club and venue assignments and details, including creation
and updates for venues, club information, and associated venue metadata.
"""

from django import forms
from .models import ClubInfo, ClubVenue, Venue, VenueInfo, ClubReview


class AssignClubVenueForm(forms.ModelForm):
    """
    Form for assigning a new venue to a club.

    Filters out venues already assigned to the specified club from the
    dropdown options.

    Requires a 'club' keyword argument when instantiated for filtering logic
    to function correctly.
    """

    class Meta:
        model = ClubVenue
        fields = [
            "venue",
        ]
        labels = {
            "venue": "Choose a venue",
        }

    def __init__(self, *args, **kwargs):
        """
        Initialises the form and filters the venue queryset to exclude venues
        already assigned to the provided 'club'.
        """
        # Pass custom 'club' argument when form is initialised
        club = kwargs.pop("club", None)
        super().__init__(*args, **kwargs)

        # Exclude venues already assigned to the club from the dropdown
        if club:
            assigned_venue_ids = ClubVenue.objects.filter(
                club=club
            ).values_list("venue_id", flat=True)
            self.fields["venue"].queryset = Venue.objects.exclude(
                id__in=assigned_venue_ids
            )


class ClubReviewForm(forms.ModelForm):
    """
    Form for creating or editing a club review.
    """

    class Meta:
        model = ClubReview
        fields = [
            "score",
            "headline",
            "review_text",
        ]
        labels = {
            "score": "Rating (1-5 stars)",
            "headline": "Review Title",
            "review_text": "Your Review",
        }
        widgets = {
            "score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "headline": forms.TextInput(attrs={"maxlength": 100}),
            "review_text": forms.Textarea(attrs={"rows": 10}),
        }


class CreateVenueForm(forms.ModelForm):
    """
    Form for creating a new venue.

    This form only includes the venue name and is typically used for
    the initial venue creation step. Other venue information is submitted
    via the UpdateVenueInfoForm.
    """

    class Meta:
        model = Venue
        fields = ["name"]
        help_texts = {
            "name": "This cannot be changed after the venue is created."
        }


class UpdateClubInfoForm(forms.ModelForm):
    """
    Form for submitting information about a club.

    Includes fields for contact details, club website, session description,
    skill levels supported and checklist criteria.
    """

    class Meta:
        model = ClubInfo
        fields = [
            "contact_name",
            "contact_email",
            "contact_phone",
            "website",
            "description",
            "session_info",
            "image",
            "beginners",
            "intermediates",
            "advanced",
            "kids",
            "adults",
            "coaching",
            "league",
            "equipment_provided",
            "membership_required",
            "free_taster",
        ]
        labels = {
            "contact_name": "Contact Name",
            "contact_email": "Contact Email",
            "contact_phone": "Contact Phone",
            "website": "Club Website",
            "session_info": "Session Info",
            "beginners": "Suitable for beginners",
            "intermediates": "Suitable for intermediate level players",
            "advanced": "Suitable for advanced level players",
            "kids": "Suitable for kids",
            "adults": "Suitable for adults",
            "coaching": "Coaching is available",
            "league": "Club participates in the league",
            "equipment_provided": "Equipment is provided",
            "membership_required": "Membership is required",
            "free_taster": "Free taster sessions available",
        }
        help_texts = {
            "image": (
                "Upload an image for your club. "
                "Recommended format: landscape, 1200x800px, JPG or PNG."
            ),
        }
        widgets = {
            "contact_phone": forms.TextInput(
                attrs={"placeholder": "(optional)"}
            ),
            "website": forms.TextInput(attrs={"placeholder": "(optional)"}),
        }


class UpdateVenueInfoForm(forms.ModelForm):
    """
    Form for submitting venue information such as address, number of tables
    and parking information.
    """

    class Meta:
        model = VenueInfo
        fields = [
            "street_address",
            "address_line_2",
            "city",
            "county",
            "postcode",
            "num_tables",
            "parking_info",
        ]
        labels = {
            "street_address": "Street",
            "address_line_2": "Address Line 2",
            "parking_info": "Parking Info",
            "num_tables": "Number of Tables",
        }
        widgets = {
            "address_line_2": forms.TextInput(
                attrs={"placeholder": "(optional)"}
            )
        }
