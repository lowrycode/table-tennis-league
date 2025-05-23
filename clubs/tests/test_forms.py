from django.test import TestCase
from clubs.forms import (
    UpdateClubInfoForm,
    AssignClubVenueForm,
    UpdateVenueInfoForm,
    CreateVenueForm,
)
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


class UpdateVenueInfoFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "street_address": "123 Main Street",
            "address_line_2": "Apartment 2",
            "city": "York",
            "county": "Yorkshire",
            "postcode": "YO1 1AA",
            "num_tables": 6,
            "parking_info": "Ample parking available",
        }

    def test_form_field_labels(self):
        form = UpdateVenueInfoForm()
        self.assertEqual(form.fields["street_address"].label, "Street")
        self.assertEqual(
            form.fields["address_line_2"].label, "Address Line 2 (optional)"
        )
        self.assertEqual(form.fields["num_tables"].label, "Number of tables")

    def test_valid_form(self):
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_required_fields(self):
        data = {
            "street_address": "",
            "address_line_2": "",
            "city": "",
            "county": "",
            "postcode": "",
            "num_tables": "",
            "parking_info": "",
        }
        form = UpdateVenueInfoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("street_address", form.errors)
        self.assertIn("city", form.errors)
        self.assertIn("postcode", form.errors)
        self.assertIn("num_tables", form.errors)
        self.assertNotIn("address_line_2", form.errors)  # Optional

    def test_optional_field_address_line_2_can_be_blank(self):
        self.valid_data["address_line_2"] = ""
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_negative_num_tables(self):
        self.valid_data["num_tables"] = -1
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("num_tables", form.errors)

    def test_invalid_form_with_non_integer_num_tables(self):
        self.valid_data["num_tables"] = "five"
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("num_tables", form.errors)


class CreateVenueFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Example Venue",
        }

    def test_form_field_labels(self):
        form = CreateVenueForm()
        self.assertEqual(form.fields["name"].label, "Name")

    def test_form_field_help_texts(self):
        form = CreateVenueForm()
        self.assertEqual(
            form.fields["name"].help_text,
            "This cannot be changed after the venue is created.",
        )

    def test_valid_form(self):
        form = CreateVenueForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_name(self):
        data = {
            "name": "",
        }
        form = CreateVenueForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_invalid_form_with_duplicate_venue_name(self):
        Venue.objects.create(name=self.valid_data["name"])
        form = CreateVenueForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(
            form.errors["name"], ["Venue with this Name already exists."]
        )
