from django.test import TestCase
from clubs.forms import (
    UpdateClubInfoForm,
    AssignClubVenueForm,
    UpdateVenueInfoForm,
    CreateVenueForm,
    ClubReviewForm,
)
from clubs.models import Club, Venue, ClubVenue


class UpdateClubInfoFormTests(TestCase):
    """
    Unit tests for the UpdateClubInfoForm to ensure proper validation and
    labeling.
    """
    def setUp(self):
        """
        Set up a valid form data dictionary used in multiple test cases.
        """
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
        """
        Verify form fields have the correct labels.
        """
        form = UpdateClubInfoForm()
        self.assertEqual(
            form.fields["website"].label, "Club Website"
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
        self.assertEqual(form.fields["kids"].label, "Suitable for kids")
        self.assertEqual(form.fields["adults"].label, "Suitable for adults")
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
        """
        Verify form is valid when all required fields are correctly filled.
        """
        form = UpdateClubInfoForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_fields(self):
        """
        Verify form is invalid when required fields are missing.
        """
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
        """
        Verify form is invalid when the email format is incorrect.
        """
        self.data["contact_email"] = "not.an.email"
        form = UpdateClubInfoForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertIn("contact_email", form.errors)


class AssignClubVenueFormTests(TestCase):
    """
    Unit tests for the AssignClubVenueForm to ensure correct labels, filtering
    and venue assignment behaviour.
    """
    def setUp(self):
        """
        Set up test data with one club and two venues for use across tests.
        """
        self.club = Club.objects.create(name="Test Club")
        self.venue_1 = Venue.objects.create(name="Venue 1")
        self.venue_2 = Venue.objects.create(name="Venue 2")

    def test_form_field_label(self):
        """
        Verify form displays correct label for the venue field.
        """
        form = AssignClubVenueForm(club=self.club)
        self.assertEqual(form.fields["venue"].label, "Choose a venue")

    def test_form_excludes_already_assigned_venues(self):
        """
        Verify the form filters out venues that have already been assigned
        to the given club.
        """
        ClubVenue.objects.create(club=self.club, venue=self.venue_1)
        form = AssignClubVenueForm(club=self.club)
        self.assertNotIn(self.venue_1, form.fields["venue"].queryset)
        self.assertIn(self.venue_2, form.fields["venue"].queryset)

    def test_form_includes_all_venues_if_none_assigned(self):
        """
        Verify the form includes all venues when the club has no assigned
        venues.
        """
        form = AssignClubVenueForm(club=self.club)
        self.assertIn(self.venue_1, form.fields["venue"].queryset)
        self.assertIn(self.venue_2, form.fields["venue"].queryset)

    def test_form_valid_when_venue_is_available(self):
        """
        Verify the form is valid when a selectable venue is submitted.
        """
        form_data = {"venue": self.venue_1.id}
        form = AssignClubVenueForm(data=form_data, club=self.club)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_venue_is_not_in_queryset(self):
        """
        Verify the form is invalid if a venue already assigned to the club
        is submitted.
        """
        # Assign venue_1 so it is excluded from queryset
        ClubVenue.objects.create(club=self.club, venue=self.venue_1)
        form_data = {"venue": self.venue_1.id}
        form = AssignClubVenueForm(data=form_data, club=self.club)
        self.assertFalse(form.is_valid())
        self.assertIn("venue", form.errors)


class UpdateVenueInfoFormTests(TestCase):
    """
    Unit tests for the UpdateVenueInfoForm to validate field labels,
    required fields and input constraints.
    """
    def setUp(self):
        """
        Set up a valid data dictionary used for multiple form tests.
        """
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
        """
        Verify form fields display the correct labels.
        """
        form = UpdateVenueInfoForm()
        self.assertEqual(form.fields["street_address"].label, "Street")
        self.assertEqual(
            form.fields["address_line_2"].label, "Address Line 2"
        )
        self.assertEqual(form.fields["num_tables"].label, "Number of Tables")

    def test_valid_form(self):
        """
        Verify form is valid when all required fields are filled correctly.
        """
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_required_fields(self):
        """
        Verify form is invalid when required fields are missing.
        """
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
        """
        Verify form is valid when the optional address_line_2 field is
        left blank.
        """
        self.valid_data["address_line_2"] = ""
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_negative_num_tables(self):
        """
        Verify form is invalid when num_tables is a negative number.
        """
        self.valid_data["num_tables"] = -1
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("num_tables", form.errors)

    def test_invalid_form_with_non_integer_num_tables(self):
        """
        Verify form is invalid when num_tables is not an integer.
        """
        self.valid_data["num_tables"] = "five"
        form = UpdateVenueInfoForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("num_tables", form.errors)


class CreateVenueFormTests(TestCase):
    """
    Unit tests for the CreateVenueForm to validate field labels, help texts,
    required fields and duplicate name handling.
    """
    def setUp(self):
        """
        Set up a valid data dictionary used in multiple test cases.
        """
        self.valid_data = {
            "name": "Example Venue",
        }

    def test_form_field_labels(self):
        """
        Verify form field displays the correct label.
        """
        form = CreateVenueForm()
        self.assertEqual(form.fields["name"].label, "Name")

    def test_form_field_help_texts(self):
        """
        Verify form field displays the correct help text.
        """
        form = CreateVenueForm()
        self.assertEqual(
            form.fields["name"].help_text,
            "This cannot be changed after the venue is created.",
        )

    def test_valid_form(self):
        """
        Verify form is valid when required fields are correctly filled.
        """
        form = CreateVenueForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_name(self):
        """
        Verify form is invalid when the name field is missing.
        """
        data = {
            "name": "",
        }
        form = CreateVenueForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_invalid_form_with_duplicate_venue_name(self):
        """
        Verify form is invalid when a venue with the same name already exists.
        """
        Venue.objects.create(name=self.valid_data["name"])
        form = CreateVenueForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(
            form.errors["name"], ["Venue with this Name already exists."]
        )


class ClubReviewFormTests(TestCase):
    """
    Unit tests for the ClubReviewForm to validate field labels, required
    fields, score range validation and general form validity.
    """

    def setUp(self):
        """
        Set up a valid data dictionary used in multiple tests.
        """
        self.valid_data = {
            "score": 4,
            "headline": "Great club!",
            "review_text": "Really enjoyed the atmosphere.",
        }

    def test_form_field_labels(self):
        """
        Verify form fields display the correct labels.
        """
        form = ClubReviewForm()
        self.assertEqual(form.fields["score"].label, "Rating (1-5 stars)")
        self.assertEqual(form.fields["headline"].label, "Review Title")
        self.assertEqual(form.fields["review_text"].label, "Your Review")

    def test_valid_form(self):
        """
        Verify form is valid when all required fields are correctly filled.
        """
        form = ClubReviewForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_fields(self):
        """
        Verify form is invalid when required fields are missing.
        """
        form = ClubReviewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("score", form.errors)
        self.assertIn("headline", form.errors)
        self.assertIn("review_text", form.errors)

    def test_invalid_form_score_below_minimum(self):
        """
        Verify form is invalid when score is below the minimum allowed (1).
        """
        data = self.valid_data.copy()
        data["score"] = 0
        form = ClubReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("score", form.errors)

    def test_invalid_form_score_above_maximum(self):
        """
        Verify form is invalid when score is above the maximum allowed (5).
        """
        data = self.valid_data.copy()
        data["score"] = 6
        form = ClubReviewForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("score", form.errors)
