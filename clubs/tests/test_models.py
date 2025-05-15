from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, ClubInfo


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
        long_name = "A" * 101
        club = Club(name=long_name)
        with self.assertRaises(ValidationError):
            club.full_clean()


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
        self.assertEqual(str(self.club_info), self.club_info.club.name)

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
            "approved": False,
        }

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, field, is_required)

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
            helper_test_boolean_default(
                field, default_value, self.info_data.copy()
            )

    # Tests for club field
    def test_club_field_one_to_one(self):
        club_info2 = ClubInfo(**self.info_data)  # linking to same club again
        with self.assertRaises(ValidationError):
            club_info2.full_clean()

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
        self.assertEqual(self.club.info, self.club_info)

    # Tests for contact_name field
    def test_contact_name_max_length(self):
        # Check valid at threshold
        self.club_info.contact_name = "a" * 100
        self.club_info.full_clean()

        # Check invalid above threshold
        self.club_info.contact_name = "a" * 101
        with self.assertRaises(ValidationError):
            self.club_info.full_clean()

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


# Helper functions
def helper_test_boolean_default(field_name, default_value, info_data):
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


def helper_test_required_fields(test_case, field_name, is_required):
    club_info = ClubInfo()
    with test_case.assertRaises(ValidationError) as cm:
        club_info.full_clean()
    errors = cm.exception.message_dict

    if is_required:
        test_case.assertIn(
            field_name, errors, msg=f"{field_name} should be required"
        )
    else:
        test_case.assertNotIn(
            field_name, errors, msg=f"{field_name} should not be required"
        )
