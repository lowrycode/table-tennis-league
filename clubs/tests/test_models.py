from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from clubs.models import Club, ClubInfo, Venue, VenueInfo, ClubVenue, ClubAdmin

User = get_user_model()


class ClubTests(TestCase):
    """
    Unit tests for the Club model to verify name constraints and
    string representation.
    """

    def setUp(self):
        """
        Set up a sample Club instance for use in multiple test cases.
        """
        self.club_name = "My Test Club"
        self.club = Club.objects.create(name=self.club_name)

    def test_string_representation(self):
        """
        Verify string representation of a Club instance returns its name.
        """
        self.assertEqual(str(self.club), self.club_name)

    def test_club_name_must_be_unique(self):
        """
        Verify creating a Club with a duplicate name raises a ValidationError.
        """
        duplicate_club = Club(name=self.club_name)
        with self.assertRaises(ValidationError):
            duplicate_club.full_clean()

    def test_club_name_required(self):
        """
        Verify name field is required.
        """
        club = Club(name="")
        with self.assertRaises(ValidationError):
            club.full_clean()

    def test_club_name_max_length(self):
        """
        Verify name field respects the maximum length constraint.
        """
        # Valid length should pass without error
        name = "A" * 100
        club1 = Club(name=name)
        club1.full_clean()

        # Invalid length (too long) should raise an error
        long_name = "A" * 101
        club2 = Club(name=long_name)
        with self.assertRaises(ValidationError):
            club2.full_clean()


class ClubInfoTests(TestCase):
    """
    Unit tests for the ClubInfo model to verify field constraints,
    relationships and default behaviours.
    """

    def setUp(self):
        """
        Set up a Club instance and associated valid ClubInfo data for use in
        multiple tests.
        """
        self.club = Club.objects.create(name="My Test Club")
        self.info_data = {
            "club": self.club,
            "image": "",
            "website": "https://www.example.com",
            "contact_name": "Joe Bloggs",
            "contact_email": "example@example.com",
            "contact_phone": "01234556778",
            "description": "This club is the best!",
            "session_info": "We do every night of the week.",
        }
        self.club_info = ClubInfo.objects.create(**self.info_data)

    def test_valid_setup_info_data(self):
        """
        Verify initial test data for ClubInfo is valid.
        """
        # These should pass without raising errors
        self.club_info.full_clean()
        self.club_info.save()

    def test_string_representation(self):
        """
        Verify string representation includes the associated club name.
        """
        self.assertIn(self.club_info.club.name, str(self.club_info))

    # Multi-field tests
    def test_required_fields(self):
        """
        Verify that required and optional fields behave as expected.
        """
        required_fields = {
            "club": True,
            "image": False,
            "website": False,
            "contact_name": True,
            "contact_email": True,
            "contact_phone": False,
            "description": True,
            "session_info": True,
            "beginners": False,
            "intermediates": False,
            "advanced": False,
            "kids": False,
            "adults": False,
            "coaching": False,
            "league": False,
            "equipment_provided": False,
            "membership_required": False,
            "free_taster": False,
            "created_on": False,
            "approved": False,
        }

        test_object = ClubInfo()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """
        Verify fields with max length constraints are properly enforced.
        """
        fields = {
            "contact_name": 100,
        }

        # Check each field
        for field, max_length in fields.items():
            helper_test_max_length(
                self, ClubInfo, self.info_data.copy(), field, max_length
            )

    def test_boolean_field_defaults(self):
        """Verify all boolean fields have the correct default values."""
        boolean_fields = {
            "beginners": False,
            "intermediates": False,
            "advanced": False,
            "kids": False,
            "adults": False,
            "coaching": False,
            "league": False,
            "equipment_provided": False,
            "membership_required": False,
            "free_taster": False,
            "approved": False,
        }

        # Check each field
        for field, default_value in boolean_fields.items():
            result = helper_test_boolean_default(
                field, default_value, ClubInfo, self.info_data.copy()
            )
            self.assertTrue(
                result, f"Default for {field} should be {default_value}"
            )

    # Tests for club field
    def test_club_field_many_to_one(self):
        """
        Verify that multiple ClubInfo instances can be associated with
        a single Club.
        """
        club_info2 = ClubInfo(**self.info_data)  # linking to same club again

        # These should not raise an error
        club_info2.full_clean()
        club_info2.save()

        # Check that both ClubInfos exist for the same club
        infos = ClubInfo.objects.filter(club=self.info_data["club"])
        self.assertEqual(infos.count(), 2)

    def test_club_field_cascade_delete(self):
        """
        Verify that deleting a Club cascades and deletes associated ClubInfo,
        but deleting ClubInfo does not delete the Club.
        """
        # Test correct behaviour
        self.club.delete()
        self.assertFalse(
            ClubInfo.objects.filter(id=self.club_info.id).exists()
        )

        # Set up new club and club info to test opposite behaviour
        club2 = Club.objects.create(name="My Second Club")
        info_data2 = self.info_data.copy()
        info_data2["club"] = club2
        club_info2 = ClubInfo.objects.create(**info_data2)
        self.assertTrue(ClubInfo.objects.filter(id=club_info2.id).exists())

        # Test opposite behaviour
        club_info2.delete()
        self.assertTrue(Club.objects.filter(id=club2.id).exists())

    def test_club_field_related_name(self):
        """
        Verify related_name 'club_infos' correctly links Club to ClubInfo.
        """
        self.assertEqual(self.club_info.club, self.club)
        self.assertIn(self.club_info, self.club.club_infos.all())

    # Tests for contact_phone field
    def test_invalid_phone_number(self):
        """
        Verify that the contact_phone field must be a valid UK number.
        """
        # Test not a number
        self.club_info.contact_phone = "Invalid"
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

        # Test invalid region
        self.club_info.contact_phone = "4155552671"  # US phone number
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

    # Tests for description field
    def test_description_max_length(self):
        """Verify maximum length for description field is enforced."""
        # Check valid at threshold
        self.club_info.description = "a" * 500
        self.club_info.full_clean()

        # Check invalid above threshold
        self.club_info.description = "a" * 501
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

    # Tests for session_info field
    def test_session_info_max_length(self):
        """
        Verify maximum length for session_info field is enforced.
        """
        # Check valid at threshold
        self.club_info.session_info = "a" * 500
        self.club_info.full_clean()

        # Check invalid above threshold
        self.club_info.session_info = "a" * 501
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

    # Tests for image field
    def test_image_field_defaults_to_placeholder(self):
        """
        Verify image field defaults to 'placeholder' when left blank.
        """
        # Create a new club for this test instance
        club2 = Club.objects.create(name="My Second Club")

        # Create copy of info data with amended club and image removed
        info_data = self.info_data.copy()
        info_data["club"] = club2
        info_data.pop("image", None)

        # Create ClubInfo object
        club_info = ClubInfo.objects.create(**info_data)

        # Check placeholder is recorded as default
        self.assertEqual(club_info.image, "placeholder")

    # Tests for created_on field
    def test_created_on_field_is_not_none(self):
        """
        Verify created_on field is automatically populated.
        """
        self.assertIsNotNone(self.club_info.created_on)


class VenueTests(TestCase):
    """
    Unit tests for the Venue model to verify string representation
    and field constraints.
    """

    def setUp(self):
        """Set up a Venue instance for use in tests."""
        self.venue_name = "My Test Venue"
        self.venue = Venue.objects.create(name=self.venue_name)

    def test_string_representation(self):
        """Test string representation returns the name."""
        self.assertEqual(str(self.venue), self.venue_name)

    def test_venue_name_must_be_unique(self):
        """Verify that Venue names must be unique."""
        duplicate_venue = Venue(name=self.venue_name)
        with self.assertRaises(ValidationError):
            duplicate_venue.full_clean()

    def test_venue_name_required(self):
        """Verify that Venue name is required."""
        venue = Venue(name="")
        with self.assertRaises(ValidationError):
            venue.full_clean()

    def test_venue_name_max_length(self):
        """Verify maximum length constraint on Venue name."""
        # Valid length should pass without error
        name = "A" * 100
        venue1 = Venue(name=name)
        venue1.full_clean()

        # Invalid length (too long) should raise an error
        long_name = "A" * 101
        venue2 = Venue(name=long_name)
        with self.assertRaises(ValidationError):
            venue2.full_clean()


class VenueInfoTests(TestCase):
    """
    Unit tests for the VenueInfo model to verify string representation,
    field constraints and relationships.
    """
    def setUp(self):
        """
        Set up a Venue and associated VenueInfo instance for use in tests.
        """
        self.venue = Venue.objects.create(name="My Test Venue")
        self.info_data = {
            "venue": self.venue,
            "street_address": "5 Main Street",
            "city": "York",
            "county": "Yorkshire",
            "postcode": "YO1 9NX",
            "num_tables": 5,
            "parking_info": "We have a car park outside the venue",
        }
        self.venue_info = VenueInfo.objects.create(**self.info_data)

    def test_valid_setup_info_data(self):
        """Verify initial VenueInfo setup data is valid."""
        # These should pass without raising errors
        self.venue_info.full_clean()
        self.venue_info.save()

    def test_string_representation(self):
        """Verify VenueInfo string representation includes the venue name."""
        self.assertIn(self.venue_info.venue.name, str(self.venue_info))

    # Multi-field tests
    def test_required_fields(self):
        """Verify wehether each VenueInfo fields is required or not."""
        required_fields = {
            "venue": True,
            "street_address": True,
            "address_line_2": False,
            "city": True,
            "county": True,
            "postcode": True,
            "num_tables": True,
            "parking_info": True,
        }

        # Check each field
        test_object = VenueInfo()
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """Verify max length constraints for various VenueInfo fields."""
        fields = {
            "street_address": 100,
            "address_line_2": 100,
            "city": 100,
            "county": 100,
            "postcode": 8,
            "parking_info": 500,
        }

        # Check each field
        for field, max_length in fields.items():
            helper_test_max_length(
                self, VenueInfo, self.info_data.copy(), field, max_length
            )

    def test_boolean_field_defaults(self):
        """Verify default values for boolean fields."""
        boolean_fields = {
            "meets_league_standards": False,
            "approved": False,
        }

        # Check each field
        for field, default_value in boolean_fields.items():
            result = helper_test_boolean_default(
                field, default_value, VenueInfo, self.info_data.copy()
            )
            self.assertTrue(
                result, f"Default for {field} should be {default_value}"
            )

    def test_num_fields_range(self):
        """Verify numeric range validation for num_tables."""
        # Check lower limit is valid
        self.venue_info.num_tables = 1
        self.venue_info.full_clean()

        # Check upper limit is valid
        self.venue_info.num_tables = 100
        self.venue_info.full_clean()

        # Check invalid numbers below range
        self.venue_info.num_tables = 0
        with self.assertRaises(ValidationError):
            self.venue_info.full_clean()

        self.venue_info.num_tables = -1
        with self.assertRaises(ValidationError):
            self.venue_info.full_clean()

        # Check invalid numbers above range
        self.venue_info.num_tables = 101
        with self.assertRaises(ValidationError):
            self.venue_info.full_clean()

    # Tests for venue field
    def test_venue_field_many_to_one(self):
        """Verify that multiple VenueInfos can be linked to the same Venue."""
        venue_info2 = VenueInfo(
            **self.info_data
        )  # linking to same venue again

        # These should not raise an error
        venue_info2.full_clean()
        venue_info2.save()

        # Check that both VenueInfos exist for the same venue
        infos = VenueInfo.objects.filter(venue=self.info_data["venue"])
        self.assertEqual(infos.count(), 2)

    def test_venue_field_cascade_delete(self):
        """
        Verify cascade deletion from Venue to VenueInfo but not the reverse.
        """
        # Test correct behaviour
        self.venue.delete()
        self.assertFalse(
            VenueInfo.objects.filter(id=self.venue_info.id).exists()
        )

        # Set up new venue and venue info to test opposite behaviour
        venue2 = Venue.objects.create(name="My Second Venue")
        info_data2 = self.info_data.copy()
        info_data2["venue"] = venue2
        venue_info2 = VenueInfo.objects.create(**info_data2)
        self.assertTrue(VenueInfo.objects.filter(id=venue_info2.id).exists())

        # Test opposite behaviour
        venue_info2.delete()
        self.assertTrue(Venue.objects.filter(id=venue2.id).exists())

    def test_venue_field_related_name(self):
        """Verify related name from Venue to VenueInfo."""
        self.assertEqual(self.venue_info.venue, self.venue)
        self.assertIn(self.venue_info, self.venue.venue_infos.all())

    # Tests for created_on field
    def test_created_on_field_is_not_none(self):
        """Verify created_on field is automatically populated."""
        self.assertIsNotNone(self.venue_info.created_on)


class ClubVenueTests(TestCase):
    """
    Unit tests for the ClubVenue model to verify string representation,
    required fields and relationships.
    """
    def setUp(self):
        """Set up Club, Venue, and ClubVenue instances for use in tests."""
        self.club = Club.objects.create(name="My Test Club")
        self.venue = Venue.objects.create(name="My Test Venue")
        self.data = {
            "club": self.club,
            "venue": self.venue,
        }
        self.club_venue = ClubVenue.objects.create(**self.data)

    def test_valid_setup_info_data(self):
        """Verify initial ClubVenue setup data is valid."""
        # These should pass without raising errors
        self.club_venue.full_clean()
        self.club_venue.save()

    def test_string_representation(self):
        """
        Verify ClubVenue string representation includes both club and
        venue names.
        """
        self.assertIn(self.club_venue.club.name, str(self.club_venue))
        self.assertIn(self.club_venue.venue.name, str(self.club_venue))

    # Multi-field tests
    def test_required_fields(self):
        """Verify whuch ClubVenue fields are required."""
        required_fields = {
            "club": True,
            "venue": True,
        }

        test_object = ClubVenue()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    # Tests for club field
    def test_club_venue_combination_must_be_unique(self):
        """Verify each club-venue pair must be unique."""
        # link to same club and venue again
        duplicate = ClubVenue(**self.data)

        # These should raise an error
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_club_field_cascade_delete(self):
        """Verify that deleting a club also deletes associated ClubVenue."""
        # Test correct behaviour
        self.club.delete()
        self.assertFalse(
            ClubVenue.objects.filter(id=self.club_venue.id).exists()
        )

    def test_venue_field_cascade_delete(self):
        """Verify that deleting a venue also deletes associated ClubVenue."""
        # Test correct behaviour
        self.venue.delete()
        self.assertFalse(
            ClubVenue.objects.filter(id=self.club_venue.id).exists()
        )

    def test_club_and_venue_not_deleted_when_clubvenue_deleted(self):
        """
        Verify that deleting a ClubVenue does not delete its Club or Venue.
        """
        # Create new club, venue and club_venue
        club_2 = Club.objects.create(name="My Second Club")
        venue_2 = Venue.objects.create(name="My Second Venue")
        data_2 = self.data.copy()
        data_2["club"] = club_2
        data_2["venue"] = venue_2
        club_venue_2 = ClubVenue.objects.create(**data_2)
        self.assertTrue(ClubVenue.objects.filter(id=club_venue_2.id).exists())

        # Check club and venue not deleted
        club_venue_2.delete()
        self.assertTrue(Club.objects.filter(id=club_2.id).exists())
        self.assertTrue(Venue.objects.filter(id=venue_2.id).exists())

    def test_club_field_related_name(self):
        """Verify related name from Club to ClubVenue."""
        self.assertEqual(self.club_venue.club, self.club)
        self.assertIn(self.club_venue, self.club.club_venues.all())

    def test_venue_field_related_name(self):
        """Verify related name from Venue to ClubVenue."""
        self.assertEqual(self.club_venue.venue, self.venue)
        self.assertIn(self.club_venue, self.venue.venue_clubs.all())


class ClubAdminTests(TestCase):
    """
    Unit tests for the ClubAdmin model to verify string representation,
    required fields and relationships.
    """
    def setUp(self):
        """Set up User, Club, and ClubAdmin instances for use in tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="example@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="My Test Club")
        self.admin = ClubAdmin.objects.create(user=self.user, club=self.club)

    def test_valid_setup_info_data(self):
        """Verify initial ClubAdmin setup data is valid."""
        # These should pass without raising errors
        self.admin.full_clean()
        self.admin.save()

    def test_string_representation(self):
        """
        Verify ClubAdmin string representation includes user and club names.
        """
        self.assertEqual(
            str(self.admin), f"{self.user.username} for {self.club.name}"
        )

    # Multi-field tests
    def test_required_fields(self):
        """Verify which ClubAdmin fields are required."""
        required_fields = {
            "user": True,
            "club": True,
        }

        test_object = ClubAdmin()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    # Tests for relationships
    def test_user_cannot_have_multiple_club_admins(self):
        """Verify that a user can only be admin for one club."""
        self.club_2 = Club.objects.create(name="Second Test Club")
        with self.assertRaises(IntegrityError):
            ClubAdmin.objects.create(user=self.user, club=self.club_2)

    def test_club_can_have_multiple_admins(self):
        """Verify that a club can have multiple administrators."""
        user_2 = User.objects.create_user(
            username="seconduser",
            email="user2@example.com",
            password="test123",
        )
        ClubAdmin.objects.create(user=user_2, club=self.club)
        self.assertEqual(self.club.admins.count(), 2)

    def test_deleting_user_deletes_club_admin(self):
        """Verify that deleting a user deletes their ClubAdmin entry."""
        self.assertTrue(ClubAdmin.objects.filter(pk=self.admin.pk).exists())
        self.user.delete()
        self.assertFalse(ClubAdmin.objects.filter(pk=self.admin.pk).exists())

    def test_deleting_club_deletes_club_admin(self):
        """Verify that deleting a club deletes its ClubAdmin entries."""
        self.assertTrue(ClubAdmin.objects.filter(pk=self.admin.pk).exists())
        self.club.delete()
        self.assertFalse(ClubAdmin.objects.filter(pk=self.admin.pk).exists())


# Helper functions
def helper_test_boolean_default(field_name, default_value, model, info_data):
    """
    Test that a boolean field has the correct default value.

    Args:
        field_name (str): The name of the boolean field to test.
        default_value (bool): The expected default value of the field.
        model (Model): The Django model class to test.
        info_data (dict): Dictionary of valid model data for required fields.

    Returns:
        bool: True if the field's value matches the default; False otherwise.
    """
    # Amend info_data
    info_data.pop(field_name, None)

    # Create test_object from info_data
    test_object = model.objects.create(**info_data)

    # Check placeholder is recorded as default
    result = getattr(test_object, field_name) == default_value

    # Return result
    return result


def helper_test_required_fields(
    test_case, test_object, field_name, is_required
):
    """
    Assert that a field is correctly assigned as required or optional.

    Args:
        test_case (TestCase): The test case instance calling this helper.
        test_object (Model): The Django model instance to validate.
        field_name (str): The name of the field being tested.
        is_required (bool): Indicates whether field should be required or not

    Raises:
        AssertionError: If field's validation does not match expectations.
    """
    with test_case.assertRaises(ValidationError) as cm:
        test_object.full_clean()
    errors = cm.exception.message_dict

    model_name = test_object.__class__.__name__

    if is_required:
        test_case.assertIn(
            field_name,
            errors,
            msg=f"{field_name} should be required in {model_name}",
        )
    else:
        test_case.assertNotIn(
            field_name,
            errors,
            msg=f"{field_name} should not be required in {model_name}",
        )


def helper_test_max_length(
    test_case, model, info_data, field_name, max_length
):
    """
    Validate that a field enforces its maximum length constraint.

    Args:
        test_case (TestCase): The test case instance calling this helper.
        model (Model): The Django model class to test.
        info_data (dict): Dictionary of valid model data.
        field_name (str): The name of the field being tested.
        max_length (int): The maximum allowed length of the field.

    Raises:
        ValidationError: If the field value exceeds the defined max_length.
    """
    # Create object
    test_object = model.objects.create(**info_data)

    # Check valid at threshold
    setattr(test_object, field_name, "a" * max_length)
    test_object.full_clean()

    # Check invalid above threshold
    setattr(test_object, field_name, "a" * (max_length + 1))
    with test_case.assertRaises(ValidationError):
        test_object.full_clean()
