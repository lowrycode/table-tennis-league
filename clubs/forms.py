from django import forms
from .models import ClubInfo, ClubVenue, Venue, VenueInfo


class UpdateClubInfoForm(forms.ModelForm):
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
            "website": "Club website (optional)",
            "beginners": "Suitable for beginners",
            "intermediates": "Suitable for intermediate level players",
            "advanced": "Suitable for advanced level players",
            "kids": "Kids are welcome",
            "adults": "Adults are welcome",
            "coaching": "Coaching is available",
            "league": "Club participates in the league",
            "equipment_provided": "Equipment is provided",
            "membership_required": "Membership is required",
            "free_taster": "Free taster sessions available",
        }


class AssignClubVenueForm(forms.ModelForm):
    class Meta:
        model = ClubVenue
        fields = [
            "venue",
        ]
        labels = {
            "venue": "Choose a venue",
        }

    def __init__(self, *args, **kwargs):
        # Pass custom 'club' argument when form is initialised
        club = kwargs.pop(
            "club", None
        )
        super().__init__(*args, **kwargs)

        # Exclude venues already assigned to the club from the dropdown
        if club:
            assigned_venue_ids = ClubVenue.objects.filter(
                club=club
            ).values_list("venue_id", flat=True)
            self.fields["venue"].queryset = Venue.objects.exclude(
                id__in=assigned_venue_ids
            )


class UpdateVenueInfoForm(forms.ModelForm):
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
            "address_line_2": "Address Line 2 (optional)",
            "num_tables": "Number of tables",
        }
