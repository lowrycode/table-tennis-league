from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club


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