from django.test import TestCase
from clubs.forms import UpdateClubInfoForm, AssignClubVenueForm
from clubs.models import Club, Venue, ClubVenue


class UpdateClubInfoFormTests(TestCase):
    def setUp(self):
        self.data = {
            "contact_name": "Joe Bloggs",
            "contact_email": "joe@example.com",
            "contact_phone": "",
            "website": "www.example.com",
            "description": "My club is great!",
            "session_info": "We play every night of the week.",
            "image": None,
            "beginners": True,
            "intermediates": True,
            "advanced": True,
            "kids": True,
            "adults": True,
            "coaching": True,
            "league": True,
            "equipment_provided": True,
            "membership_required": True,
            "free_taster": True,
        }

    def test_form_field_labels(self):
        form = UpdateClubInfoForm()
        self.assertEqual(
            form.fields["website"].label, "Club website (optional)"
        )
        self.assertEqual(
            form.fields["beginners"].label, "Suitable for beginners"
        )
        self.assertEqual(
            form.fields["intermediates"].label,
            "Suitable for intermediate level players",
        )
        self.assertEqual(
            form.fields["advanced"].label,
            "Suitable for advanced level players",
        )
        self.assertEqual(form.fields["kids"].label, "Kids are welcome")
        self.assertEqual(form.fields["adults"].label, "Adults are welcome")
        self.assertEqual(
            form.fields["coaching"].label, "Coaching is available"
        )
        self.assertEqual(
            form.fields["league"].label, "Club participates in the league"
        )
        self.assertEqual(
            form.fields["equipment_provided"].label, "Equipment is provided"
        )
        self.assertEqual(
            form.fields["membership_required"].label, "Membership is required"
        )
        self.assertEqual(
            form.fields["free_taster"].label, "Free taster sessions available"
        )

    def test_valid_form(self):
        form = UpdateClubInfoForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_fields(self):
        data = {
            "contact_name": "",
            "contact_email": "",
            "contact_phone": "",
            "website": "",
            "description": "",
            "session_info": "",
            "image": None,
        }
        form = UpdateClubInfoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("contact_name", form.errors)
        self.assertIn("contact_email", form.errors)
        self.assertNotIn("contact_phone", form.errors)
        self.assertNotIn("website", form.errors)
        self.assertIn("description", form.errors)
        self.assertIn("session_info", form.errors)
        self.assertNotIn("image", form.errors)

    def test_invalid_form_with_bad_email_format(self):
        self.data["contact_email"] = "not.an.email"
        form = UpdateClubInfoForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertIn("contact_email", form.errors)


class AssignClubVenueFormTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="Test Club")
        self.venue_1 = Venue.objects.create(name="Venue 1")
        self.venue_2 = Venue.objects.create(name="Venue 2")

    def test_form_field_label(self):
        form = AssignClubVenueForm(club=self.club)
        self.assertEqual(form.fields["venue"].label, "Choose a venue")

    def test_form_excludes_already_assigned_venues(self):
        ClubVenue.objects.create(club=self.club, venue=self.venue_1)
        form = AssignClubVenueForm(club=self.club)
        self.assertNotIn(self.venue_1, form.fields["venue"].queryset)
        self.assertIn(self.venue_2, form.fields["venue"].queryset)

    def test_form_includes_all_venues_if_none_assigned(self):
        form = AssignClubVenueForm(club=self.club)
        self.assertIn(self.venue_1, form.fields["venue"].queryset)
        self.assertIn(self.venue_2, form.fields["venue"].queryset)

    def test_form_valid_when_venue_is_available(self):
        form_data = {"venue": self.venue_1.id}
        form = AssignClubVenueForm(data=form_data, club=self.club)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_venue_is_not_in_queryset(self):
        # Assign venue_1 so it is excluded from queryset
        ClubVenue.objects.create(club=self.club, venue=self.venue_1)
        form_data = {"venue": self.venue_1.id}
        form = AssignClubVenueForm(data=form_data, club=self.club)
        self.assertFalse(form.is_valid())
        self.assertIn("venue", form.errors)
