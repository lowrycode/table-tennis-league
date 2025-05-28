from django import forms
from .models import ClubInfo, ClubVenue, Venue, VenueInfo


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


class CreateVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ["name"]
        help_texts = {
            "name": "This cannot be changed after the venue is created."
        }


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
        widgets = {
            "contact_phone": forms.TextInput(
                attrs={"placeholder": "(optional)"}
            ),
            "website": forms.TextInput(attrs={"placeholder": "(optional)"}),
        }


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
            "address_line_2": "Address Line 2",
            "parking_info": "Parking Info",
            "num_tables": "Number of Tables",
        }
        widgets = {
            "address_line_2": forms.TextInput(
                attrs={"placeholder": "(optional)"}
            )
        }
