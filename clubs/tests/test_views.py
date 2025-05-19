from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from clubs.models import Club, ClubInfo, Venue, VenueInfo, ClubVenue, ClubAdmin

User = get_user_model()


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
        self.base_club_info_data = {
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
        self.club_info_data_1 = self.base_club_info_data.copy()
        self.club_info_data_1["club"] = self.club_1
        self.club_info_data_1["contact_name"] = "Club 1 contact"
        self.club_info_data_1["description"] = "Club 1 is approved"
        self.club_info_1 = ClubInfo.objects.create(**self.club_info_data_1)

        self.club_info_data_2 = self.base_club_info_data.copy()
        self.club_info_data_2["club"] = self.club_2
        self.club_info_data_2["contact_name"] = "Club 2 contact"
        self.club_info_data_2["description"] = "Club 2 is NOT approved"
        self.club_info_data_2["approved"] = False
        self.club_info_2 = ClubInfo.objects.create(**self.club_info_data_2)

        self.club_info_data_3 = self.base_club_info_data.copy()
        self.club_info_data_3["club"] = self.club_3
        self.club_info_data_3["contact_name"] = "Club 3 contact"
        self.club_info_data_3["description"] = "Club 3 is approved"
        self.club_info_3 = ClubInfo.objects.create(**self.club_info_data_3)

        # Create Venue objects
        self.venue_1 = Venue.objects.create(name="York Venue 1")
        self.venue_2 = Venue.objects.create(name="Durham Venue 1")
        self.venue_3 = Venue.objects.create(name="Newcastle Venue 1")

        # Base VenueInfo data
        self.base_venue_info_data = {
            "venue": None,
            "street_address": "1 Main Street",
            "address_line_2": "",
            "city": "York",
            "county": "Yorkshire",
            "postcode": "YO1 1HA",
            "num_tables": 5,
            "parking_info": "There is a free carpark at the venue",
            "meets_league_standards": True,
            "approved": True,
        }

        # Create VenueInfo objects
        self.venue_info_data_1 = self.base_venue_info_data.copy()
        self.venue_info_data_1["venue"] = self.venue_1
        self.venue_info_1 = VenueInfo.objects.create(**self.venue_info_data_1)

        self.venue_info_data_2 = self.base_venue_info_data.copy()
        self.venue_info_data_2["venue"] = self.venue_2
        self.venue_info_data_2["city"] = "Durham"
        self.venue_info_data_2["county"] = "County Durham"
        self.venue_info_data_2["postcode"] = "DH1 3SE"
        self.venue_info_data_2["approved"] = True
        self.venue_info_2 = VenueInfo.objects.create(**self.venue_info_data_2)

        self.venue_info_data_3 = self.base_venue_info_data.copy()
        self.venue_info_data_3["venue"] = self.venue_3
        self.venue_info_data_3["city"] = "Newcastle"
        self.venue_info_data_3["county"] = "Tyne and Wear"
        self.venue_info_data_3["postcode"] = "NE1 7RU"
        self.venue_info_3 = VenueInfo.objects.create(**self.venue_info_data_3)

        # Create ClubVenue objects
        self.club_venue_1 = ClubVenue.objects.create(
            club=self.club_1, venue=self.venue_1
        )
        self.club_venue_2 = ClubVenue.objects.create(
            club=self.club_2, venue=self.venue_2
        )
        self.club_venue_3 = ClubVenue.objects.create(
            club=self.club_3, venue=self.venue_3
        )

    # Club Info
    def test_page_displays_placeholder_when_no_approved_clubs(self):
        ClubInfo.objects.all().delete()
        Club.objects.all().delete()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "No clubs found.")

    def test_page_displays_contact_names(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_name)

    def test_page_displays_contact_email(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_email)

    def test_page_displays_contact_phone(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_phone)

    def test_page_displays_club_description(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.description)

    def test_page_displays_placeholder_image_for_missing_image(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "<picture>")
        self.assertContains(response, 'alt="No club image provided"')
        self.assertContains(response, "placeholder.webp")
        self.assertContains(response, "placeholder.jpg")

    def test_page_displays_image_when_provided(self):
        # simulate non-placeholder
        self.club_info_1.image = "custom-image.jpg"
        self.club_info_1.save()

        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "custom-image.jpg")
        self.assertContains(response, f'alt="{self.club_1.name} image"')

    def test_page_displays_club_session_info(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "Sessions</h4>")
        self.assertContains(response, self.club_info_1.session_info)

    def test_page_displays_checkboxes(self):
        # Ensure all checkboxes should appear
        self.club_info_1.beginners = True
        self.club_info_1.intermediates = True
        self.club_info_1.advanced = True
        self.club_info_1.kids = True
        self.club_info_1.adults = True
        self.club_info_1.coaching = True
        self.club_info_1.league = True
        self.club_info_1.equipment_provided = True
        self.club_info_1.membership_required = True
        self.club_info_1.free_taster = True
        self.club_info_1.save()

        # Check they do appear
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "fa-solid fa-square-check")
        self.assertContains(response, "Beginners")
        self.assertContains(response, "Intermediates")
        self.assertContains(response, "Advanced")
        self.assertContains(response, "Kids")
        self.assertContains(response, "Adults")
        self.assertContains(response, "Coaching")
        self.assertContains(response, "Participate in league")
        self.assertContains(response, "Equipment provided")
        self.assertContains(response, "Membership required")
        self.assertContains(response, "Free taster sessions")

    def test_page_displays_only_approved_club_info(self):
        response = self.client.get(reverse("clubs"))

        # Approved clubs should be shown
        self.assertContains(response, self.club_1.name)
        self.assertContains(response, self.club_3.name)

        # Unapproved clubs should not be shown
        self.assertNotContains(response, self.club_2.name)

    def test_page_displays_clubs_alphabetically(self):
        response = self.client.get(reverse("clubs"))
        content = response.content.decode()

        # Check both clubs listed
        self.assertContains(response, self.club_1.name)
        self.assertContains(response, self.club_3.name)

        # Find positions of approved clubs
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
        self.club_info_data_1_newer = self.base_club_info_data.copy()
        self.club_info_data_1_newer["club"] = self.club_1
        self.club_info_data_1_newer["contact_name"] = "Club 1 New Contact"

        self.club_info_1_newer = ClubInfo.objects.create(
            **self.club_info_data_1_newer
        )

        # Override created_on AFTER save for reliability
        self.club_info_1_newer.save()
        self.club_info_1_newer.created_on = (
            timezone.now() + timezone.timedelta(minutes=1)
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

    # Venue Info
    def test_page_displays_placeholder_when_no_approved_venues(self):
        self.venue_info_1.approved = False
        self.venue_info_1.save()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "No venues are currently listed.")

    def test_page_displays_venue_names(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.venue_1.name)
        # ClubInfo not approved so this venue should not display
        self.assertNotContains(response, self.venue_2.name)
        self.assertContains(response, self.venue_3.name)

    def test_page_displays_number_of_tables(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, f"{self.venue_info_1.num_tables} tables")

    def test_page_displays_venue_address(self):
        self.venue_info_1.address_line_2 = "Address Line 2"
        self.venue_info_1.save()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.venue_info_1.street_address)
        self.assertContains(response, self.venue_info_1.address_line_2)
        self.assertContains(response, self.venue_info_1.city)
        self.assertContains(response, self.venue_info_1.county)
        self.assertContains(response, self.venue_info_1.postcode)

    def test_page_displays_parking_info(self):
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.venue_info_1.parking_info)

    def test_page_displays_only_approved_venue_info(self):
        # Unapprove venue 1
        self.venue_info_1.approved = False
        self.venue_info_1.save()

        response = self.client.get(reverse("clubs"))

        # Check approved venues are displayed
        # note: although venue 2 is approved the club info is not
        self.assertContains(response, self.venue_3.name)

        # Check unapproved venues are not displayed
        self.assertNotContains(response, self.venue_1.name)

    def test_page_displays_venues_alphabetically(self):
        # Create additional venues
        first_venue = self.venue_1
        second_venue = Venue.objects.create(name="Another York Venue 2")
        third_venue = Venue.objects.create(name="Venue 3 for York")

        # Create venue infos (otherwise venue won't be displayed)
        second_venue_data = self.base_venue_info_data.copy()
        second_venue_data["venue"] = second_venue
        second_venue_data["street_address"] = "Second street"
        second_venue_info = VenueInfo.objects.create(**second_venue_data)

        third_venue_data = self.base_venue_info_data.copy()
        third_venue_data["venue"] = third_venue
        third_venue_data["street_address"] = "Third street"
        third_venue_info = VenueInfo.objects.create(**third_venue_data)

        # Assign venues to club 1 (York)
        self.second_club_venue = ClubVenue.objects.create(
            club=self.club_1, venue=second_venue
        )
        self.third_club_venue = ClubVenue.objects.create(
            club=self.club_1, venue=third_venue
        )

        # Get request
        response = self.client.get(reverse("clubs"))
        content = response.content.decode()

        # Check all venues listed for club 1 (York)
        self.assertContains(response, first_venue.name)
        self.assertContains(response, second_venue.name)
        self.assertContains(response, third_venue.name)

        # Find positions of approved clubs
        pos_first_venue = content.find(first_venue.name)  # York Venue 1
        pos_second_venue = content.find(second_venue.name)  # Another ...
        pos_third_venue = content.find(third_venue.name)  # Venue 3 for York
        self.assertTrue(
            pos_second_venue < pos_third_venue < pos_first_venue,
            msg=(
                "Venues should be listed in alphabetical order:"
                f"{second_venue.name} then {third_venue.name} then {first_venue.name}"
            ),
        )

    def test_page_displays_latest_venue_info_version(self):
        self.venue_info_1.street_address = "Old Street Address"
        self.venue_info_1.save()

        self.venue_info_data_1_newer = self.base_venue_info_data.copy()
        self.venue_info_data_1_newer["venue"] = self.venue_1
        self.venue_info_data_1_newer["street_address"] = "New Street Address"

        self.venue_info_1_newer = VenueInfo.objects.create(
            **self.venue_info_data_1_newer
        )

        # Override created_on AFTER save for reliability
        self.venue_info_1_newer.save()
        self.venue_info_1_newer.created_on = (
            timezone.now() + timezone.timedelta(minutes=1)
        )

        response = self.client.get(reverse("clubs"))

        # Most recent (approved) venue info should be shown
        self.assertContains(response, self.venue_info_1_newer.street_address)

        # Less recent (approved) venue info should not be shown
        self.assertNotContains(response, self.venue_info_1.street_address)

    def test_venue_with_no_approved_venue_info(self):
        # Delete all VenueInfos for venue_1
        VenueInfo.objects.filter(venue=self.venue_1).delete()

        response = self.client.get(reverse("clubs"))

        # Assert venue name is not in the response
        self.assertNotContains(
            response,
            self.venue_1.name,
            msg_prefix="Venue with no approved venue_info should not be shown",
        )


class ClubAdminDashboardTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")

        # Base ClubInfo data
        self.base_club_info_data = {
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

        # Create ClubInfo object
        self.club_info_data_1 = self.base_club_info_data.copy()
        self.club_info_data_1["club"] = self.club
        self.club_info_1 = ClubInfo.objects.create(**self.club_info_data_1)

        # Create Venue objects
        self.venue = Venue.objects.create(name="Test Venue Name")

        # Base VenueInfo data
        self.base_venue_info_data = {
            "venue": None,
            "street_address": "1 Main Street",
            "address_line_2": "",
            "city": "York",
            "county": "Yorkshire",
            "postcode": "YO1 1HA",
            "num_tables": 5,
            "parking_info": "There is a free carpark at the venue",
            "meets_league_standards": True,
            "approved": True,
        }

        # Create VenueInfo object
        self.venue_info_data = self.base_venue_info_data.copy()
        self.venue_info_data["venue"] = self.venue
        self.venue_info_1 = VenueInfo.objects.create(**self.venue_info_data)

        # Create ClubVenue object
        self.club_venue = ClubVenue.objects.create(
            club=self.club, venue=self.venue
        )

        # Assign ClubAdmin status
        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

    # Club Info
    def test_page_displays_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/admin_dashboard.html")
        self.assertContains(response, "Club Admin Dashboard")

    def test_page_redirects_unauthenticated_user_to_login_page(self):
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_page_redirects_authenticated_user_without_club_admin_status(self):
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )
