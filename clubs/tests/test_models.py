from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, ClubInfo, Venue, VenueInfo


class ClubTests(TestCase):
    def setUp(self):
        self.club_name = "My Test Club"
        self.club = Club.objects.create(name=self.club_name)

    def test_string_representation(self):
        self.assertEqual(str(self.club), self.club_name)

    def test_club_name_must_be_unique(self):
        duplicate_club = Club(name=self.club_name)
        with self.assertRaises(ValidationError):
            duplicate_club.full_clean()

    def test_club_name_required(self):
        club = Club(name="")
        with self.assertRaises(ValidationError):
            club.full_clean()

    def test_club_name_max_length(self):
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
    def setUp(self):
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
        # These should pass without raising errors
        self.club_info.full_clean()
        self.club_info.save()

    def test_string_representation(self):
        self.assertIn(self.club_info.club.name, str(self.club_info))

    # Multi-field tests
    def test_required_fields(self):
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
        fields = {
            "contact_name": 100,
        }

        # Check each field
        for field, max_length in fields.items():
            helper_test_max_length(
                self, ClubInfo, self.info_data.copy(), field, max_length
            )

    def test_boolean_field_defaults(self):
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
            result = helper_test_boolean_default_on_club_info(
                field, default_value, self.info_data.copy()
            )
            self.assertTrue(
                result, f"Default for {field} should be {default_value}"
            )

    # Tests for club field
    def test_club_field_many_to_one(self):
        club_info2 = ClubInfo(**self.info_data)  # linking to same club again

        # These should not raise an error
        club_info2.full_clean()
        club_info2.save()

        # Check that both ClubInfos exist for the same club
        infos = ClubInfo.objects.filter(club=self.info_data["club"])
        self.assertEqual(infos.count(), 2)

    def test_club_field_cascade_delete(self):
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
        self.assertEqual(self.club_info.club, self.club)
        self.assertIn(self.club_info, self.club.infos.all())

    # Tests for contact_phone field
    def test_invalid_phone_number(self):
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
        # Check valid at threshold
        self.club_info.description = "a" * 500
        self.club_info.full_clean()

        # Check invalid above threshold
        self.club_info.description = "a" * 501
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

    # Tests for session_info field
    def test_session_info_max_length(self):
        # Check valid at threshold
        self.club_info.session_info = "a" * 500
        self.club_info.full_clean()

        # Check invalid above threshold
        self.club_info.session_info = "a" * 501
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

    # Tests for image field
    def test_image_field_defaults_to_placeholder(self):
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
        self.assertIsNotNone(self.club_info.created_on)


class VenueTests(TestCase):
    def setUp(self):
        self.venue_name = "My Test Venue"
        self.venue = Venue.objects.create(name=self.venue_name)

    def test_string_representation(self):
        self.assertEqual(str(self.venue), self.venue_name)

    def test_venue_name_must_be_unique(self):
        duplicate_venue = Venue(name=self.venue_name)
        with self.assertRaises(ValidationError):
            duplicate_venue.full_clean()

    def test_venue_name_required(self):
        venue = Venue(name="")
        with self.assertRaises(ValidationError):
            venue.full_clean()

    def test_venue_name_max_length(self):
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
    def setUp(self):
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
        # These should pass without raising errors
        self.venue_info.full_clean()
        self.venue_info.save()

    def test_string_representation(self):
        self.assertIn(self.venue_info.venue.name, str(self.venue_info))

    # Multi-field tests
    def test_required_fields(self):
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
        boolean_fields = {
            "meets_league_standards": False,
            "approved": False,
        }

        # Check each field
        for field, default_value in boolean_fields.items():
            result = helper_test_boolean_default_generic(
                field, default_value, VenueInfo, self.info_data.copy()
            )
            self.assertTrue(
                result, f"Default for {field} should be {default_value}"
            )

    def test_num_fields_range(self):
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
        self.assertEqual(self.venue_info.venue, self.venue)
        self.assertIn(self.venue_info, self.venue.venue_infos.all())

    # Tests for created_on field
    def test_created_on_field_is_not_none(self):
        self.assertIsNotNone(self.venue_info.created_on)


# Helper functions
def helper_test_boolean_default_on_club_info(
    field_name, default_value, info_data
):
    # Create a new club for this test instance
    club = Club.objects.create(name="A Different Club Name")

    # Amend info_data
    info_data["club"] = club
    info_data.pop(field_name, None)

    # Create ClubInfo object from info_data
    club_info = ClubInfo.objects.create(**info_data)

    # Check placeholder is recorded as default
    result = getattr(club_info, field_name) == default_value

    # Tidy up and return result
    club.delete()
    return result


def helper_test_boolean_default_generic(
    field_name, default_value, model, info_data
):
    # Amend info_data
    info_data.pop(field_name, None)

    # Create ClubInfo object from info_data
    test_object = model.objects.create(**info_data)

    # Check placeholder is recorded as default
    result = getattr(test_object, field_name) == default_value

    # Return result
    return result


def helper_test_required_fields(
    test_case, test_object, field_name, is_required
):
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
    # Create object
    test_object = model.objects.create(**info_data)

    # Check valid at threshold
    setattr(test_object, field_name, "a" * max_length)
    test_object.full_clean()

    # Check invalid above threshold
    setattr(test_object, field_name, "a" * (max_length + 1))
    with test_case.assertRaises(ValidationError):
        test_object.full_clean()
