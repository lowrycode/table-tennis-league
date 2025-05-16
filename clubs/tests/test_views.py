from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from clubs.models import Club, ClubInfo


class ClubsPageStaticTests(TestCase):
    def test_page_returns_correct_status_code(self):
        response = self.client.get(reverse("clubs"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        response = self.client.get(reverse("clubs"))
        self.assertTemplateUsed(response, "clubs/clubs.html")

    def test_page_has_hidden_title(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, '<h1 class="visually-hidden"')
        self.assertContains(response, "Clubs Page")

    # club-info Section
    def test_page_contains_club_info_section(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, '<section id="club-info"')


class ClubsPageDynamicTests(TestCase):
    def setUp(self):
        # Create Club objects
        self.club_1 = Club.objects.create(name="York Club")
        self.club_2 = Club.objects.create(name="Durham Club")
        self.club_3 = Club.objects.create(name="Newcastle Club")

        # Base ClubInfo data
        self.base_data = {
            "club": None,
            "image": "",
            "website": "https://www.example.com",
            "contact_name": "Joe Bloggs",
            "contact_email": "example@example.com",
            "contact_phone": "01234556778",
            "description": "This club is the best!",
            "session_info": "We do every night of the week.",
            "approved": True,
        }

        # Create ClubInfo objects
        self.info_data_1 = self.base_data.copy()
        self.info_data_1["club"] = self.club_1
        self.info_data_1["contact_name"] = "Club 1 contact"
        self.info_data_1["description"] = "Club 1 is approved"
        self.club_info_1 = ClubInfo.objects.create(**self.info_data_1)

        self.info_data_2 = self.base_data.copy()
        self.info_data_2["club"] = self.club_2
        self.info_data_2["contact_name"] = "Club 2 contact"
        self.info_data_2["description"] = "Club 2 is NOT approved"
        self.info_data_2["approved"] = False
        self.club_info_2 = ClubInfo.objects.create(**self.info_data_2)

        self.info_data_3 = self.base_data.copy()
        self.info_data_3["club"] = self.club_3
        self.info_data_3["contact_name"] = "Club 3 contact"
        self.info_data_3["description"] = "Club 3 is approved"
        self.club_info_3 = ClubInfo.objects.create(**self.info_data_3)

    def test_page_displays_placeholder_when_no_active_clubs(self):
        ClubInfo.objects.all().delete()
        Club.objects.all().delete()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "No clubs are currently listed.")

    def test_page_displays_contact_names(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_name)

    def test_page_displays_contact_email(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_email)

    def test_page_displays_contact_phone(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_phone)

    def test_page_displays_only_approved_club_info(self):
        response = self.client.get(reverse("clubs"))

        # Active clubs should be shown
        self.assertContains(response, self.club_1.name)
        self.assertContains(response, self.club_3.name)

        # Inactive clubs should not be shown
        self.assertNotContains(response, self.club_2.name)

    def test_page_displays_clubs_alphabetically(self):
        response = self.client.get(reverse("clubs"))
        content = response.content.decode()

        # Check both clubs listed
        self.assertContains(response, self.club_1.name)
        self.assertContains(response, self.club_3.name)

        # Find positions of active clubs
        pos_club_1 = content.find(self.club_1.name)  # York Club
        pos_club_3 = content.find(self.club_3.name)  # Newcastle Club
        self.assertTrue(
            pos_club_3 < pos_club_1,
            msg=(
                f"{self.club_3.name} should come before {self.club_1.name}"
                " in alphabetical order"
            ),
        )

    def test_page_displays_latest_club_info_version(self):
        self.info_data_1_newer = self.base_data.copy()
        self.info_data_1_newer["club"] = self.club_1
        self.info_data_1_newer["contact_name"] = "Club 1 New Contact"
        self.info_data_1_newer["created_on"] = (
            timezone.now() + timezone.timedelta(minutes=1)
        )
        self.club_info_1_newer = ClubInfo.objects.create(
            **self.info_data_1_newer
        )

        response = self.client.get(reverse("clubs"))

        # Most recent (approved) club info should be shown
        self.assertContains(response, self.club_info_1_newer.contact_name)

        # Less recent (approved) club info should not be shown
        self.assertNotContains(response, self.club_info_1.contact_name)

    def test_club_with_no_club_info(self):
        self.club = Club.objects.create(name="Club not linked to ClubInfo")
        response = self.client.get(reverse("clubs"))

        self.assertNotContains(
            response,
            self.club.name,
            msg_prefix="Club with no club_info attached should not show",
        )
