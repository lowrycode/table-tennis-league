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
        }
        self.club_info = ClubInfo.objects.create(**self.info_data)

    def test_valid_setup_info_data(self):
        # These should pass without raising errors
        self.club_info.full_clean()
        self.club_info.save()

    def test_string_representation(self):
        self.assertEqual(str(self.club_info), self.club_info.club.name)

    def test_required_fields(self):
        club_info = ClubInfo()
        with self.assertRaises(ValidationError) as cm:
            club_info.full_clean()
        errors = cm.exception.message_dict

        self.assertIn("club", errors, msg="club should be required")
        self.assertNotIn("image", errors, msg="image should not be required")
        self.assertNotIn(
            "website", errors, msg="website should not be required"
        )
        self.assertIn(
            "contact_name", errors, msg="contact_name should be required"
        )
        self.assertIn(
            "contact_email", errors, msg="contact_email should be required"
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
