from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from clubs.models import Club, ClubInfo, Venue, VenueInfo, ClubVenue, ClubAdmin
from clubs.forms import UpdateClubInfoForm

User = get_user_model()


class ClubsPageStaticTests(TestCase):
    """
    Tests for static aspects of the clubs page, including structure,
    template and presence of elements.
    """

    def test_page_returns_correct_status_code(self):
        """Verify clubs page returns a 200 OK status."""
        response = self.client.get(reverse("clubs"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify correct template is used for rendering clubs page."""
        response = self.client.get(reverse("clubs"))
        self.assertTemplateUsed(response, "clubs/clubs.html")

    def test_page_has_hidden_title(self):
        """Verify clubs page includes a visually hidden h1 title."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, '<h1 class="visually-hidden"')
        self.assertContains(response, "Clubs Page")

    # club-info Section
    def test_page_contains_club_info_section(self):
        """Verify clubs page includes a section for club information."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, '<section id="club-info"')


class ClubsPageDynamicTests(TestCase):
    """
    Tests for dynamic data rendering on the clubs page based on Club,
    ClubInfo, Venue, and VenueInfo data.
    """

    def setUp(self):
        """
        Create clubs, venues and their related information for use in tests.
        """
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
        """
        Verify placeholder text is shown when there are no approved clubs.
        """
        ClubInfo.objects.all().delete()
        Club.objects.all().delete()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "No clubs found.")

    def test_page_displays_contact_names(self):
        """Verify that contact name is shown for approved club."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_name)

    def test_page_displays_contact_email(self):
        """Verify contact email is shown for approved club."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_email)

    def test_page_displays_contact_phone(self):
        """Verify contact phone number is shown for approved club."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.contact_phone)

    def test_page_displays_club_description(self):
        """Verify club description is shown for approved club."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.club_info_1.description)

    def test_page_displays_placeholder_image_for_missing_image(self):
        """
        Verify placeholder image is shown when no image is provided for a club.
        """
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "<picture>")
        self.assertContains(response, 'alt="No club image provided"')
        self.assertContains(response, "placeholder.webp")
        self.assertContains(response, "placeholder.jpg")

    def test_page_displays_image_when_provided(self):
        """Verify that the club's image appears when it is provided."""
        # simulate non-placeholder
        self.club_info_1.image = "custom-image.jpg"
        self.club_info_1.save()

        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "custom-image.jpg")
        self.assertContains(response, f'alt="{self.club_1.name} image"')

    def test_page_displays_club_session_info(self):
        """Verify session information is shown for approved club."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "Sessions</h4>")
        self.assertContains(response, self.club_info_1.session_info)

    def test_page_displays_checkboxes(self):
        """
        Verify all feature checkboxes are rendered when enabled for a club.
        """
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
        """Verify that only clubs with approved ClubInfo entries are shown."""
        response = self.client.get(reverse("clubs"))

        # Approved clubs should be shown
        self.assertContains(response, self.club_1.name)
        self.assertContains(response, self.club_3.name)

        # Unapproved clubs should not be shown
        self.assertNotContains(response, self.club_2.name)

    def test_page_displays_clubs_alphabetically(self):
        """Verify clubs are listed in alphabetical order by name."""
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
        """
        Verify most recently created ClubInfo version
        is displayed (if approved).
        """
        self.club_info_data_1_newer = self.base_club_info_data.copy()
        self.club_info_data_1_newer["club"] = self.club_1
        self.club_info_data_1_newer["contact_name"] = "Club 1 New Contact"

        self.club_info_1_newer = ClubInfo.objects.create(
            **self.club_info_data_1_newer
        )

        # Override created_on AFTER creation for reliability
        self.club_info_1_newer.created_on = (
            timezone.now() + timezone.timedelta(minutes=1)
        )
        self.club_info_1_newer.save()

        response = self.client.get(reverse("clubs"))

        # Most recent (approved) club info should be shown
        self.assertContains(response, self.club_info_1_newer.contact_name)

        # Less recent (approved) club info should not be shown
        self.assertNotContains(response, self.club_info_1.contact_name)

    def test_club_with_no_club_info(self):
        """Verify that clubs with no ClubInfo are not displayed."""
        self.club = Club.objects.create(name="Club not linked to ClubInfo")
        response = self.client.get(reverse("clubs"))

        self.assertNotContains(
            response,
            self.club.name,
            msg_prefix="Club with no club_info attached should not show",
        )

    # Venue Info
    def test_page_displays_placeholder_when_no_approved_venues(self):
        """Verify placeholder text appears when no venues are approved."""
        self.venue_info_1.approved = False
        self.venue_info_1.save()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, "No venues are currently listed.")

    def test_page_displays_venue_names(self):
        """
        Verify venue names are shown only if linked to approved ClubInfo
        and approved themselves.
        """
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.venue_1.name)
        # ClubInfo not approved so this venue should not display
        self.assertNotContains(response, self.venue_2.name)
        self.assertContains(response, self.venue_3.name)

    def test_page_displays_number_of_tables(self):
        """Verify the number of tables is shown for an approved venue."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, f"{self.venue_info_1.num_tables} tables")

    def test_page_displays_venue_address(self):
        """Verify that the full address of an approved venue is displayed."""
        self.venue_info_1.address_line_2 = "Address Line 2"
        self.venue_info_1.save()
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.venue_info_1.street_address)
        self.assertContains(response, self.venue_info_1.address_line_2)
        self.assertContains(response, self.venue_info_1.city)
        self.assertContains(response, self.venue_info_1.county)
        self.assertContains(response, self.venue_info_1.postcode)

    def test_page_displays_parking_info(self):
        """Verify that parking information is shown for venues."""
        response = self.client.get(reverse("clubs"))
        self.assertContains(response, self.venue_info_1.parking_info)

    def test_page_displays_only_approved_venue_info(self):
        """Verify that only approved VenueInfo entries appear on the page."""
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
        """
        Verify venues are displayed in alphabetical order under each club.
        """
        # Create additional venues
        first_venue = self.venue_1
        second_venue = Venue.objects.create(name="Another York Venue 2")
        third_venue = Venue.objects.create(name="Venue 3 for York")

        # Create venue infos (otherwise venue won't be displayed)
        second_venue_data = self.base_venue_info_data.copy()
        second_venue_data["venue"] = second_venue
        second_venue_data["street_address"] = "Second street"
        VenueInfo.objects.create(**second_venue_data)

        third_venue_data = self.base_venue_info_data.copy()
        third_venue_data["venue"] = third_venue
        third_venue_data["street_address"] = "Third street"
        VenueInfo.objects.create(**third_venue_data)

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
                f"{second_venue.name} then {third_venue.name}"
                f" then {first_venue.name}"
            ),
        )

    def test_page_displays_latest_venue_info_version(self):
        """
        Verify most recent VenueInfo version is shown for a venue
        (if approved).
        """
        self.venue_info_1.street_address = "Old Street Address"
        self.venue_info_1.save()

        self.venue_info_data_1_newer = self.base_venue_info_data.copy()
        self.venue_info_data_1_newer["venue"] = self.venue_1
        self.venue_info_data_1_newer["street_address"] = "New Street Address"

        self.venue_info_1_newer = VenueInfo.objects.create(
            **self.venue_info_data_1_newer
        )

        # Override created_on AFTER creation for reliability
        self.venue_info_1_newer.created_on = (
            timezone.now() + timezone.timedelta(minutes=1)
        )
        self.venue_info_1_newer.save()

        response = self.client.get(reverse("clubs"))

        # Most recent (approved) venue info should be shown
        self.assertContains(response, self.venue_info_1_newer.street_address)

        # Less recent (approved) venue info should not be shown
        self.assertNotContains(response, self.venue_info_1.street_address)

    def test_venue_with_no_approved_venue_info(self):
        """
        Verify venues with no approved VenueInfo entries are not displayed.
        """
        # Delete all VenueInfos for venue_1
        VenueInfo.objects.filter(venue=self.venue_1).delete()

        response = self.client.get(reverse("clubs"))

        # Assert venue name is not in the response
        self.assertNotContains(
            response,
            self.venue_1.name,
            msg_prefix="Venue with no approved venue_info should not be shown",
        )


class ClubsPageFilterTests(TestCase):
    """
    Tests for verifying the filtering functionality on the clubs listing page.
    """

    def setUp(self):
        """
        Create clubs, club info, venues, venue info, and club venue instances
        for use in tests.
        """
        # Create Club objects
        self.club_1 = Club.objects.create(name="Club 1")
        self.club_2 = Club.objects.create(name="Club 2")
        self.club_3 = Club.objects.create(name="Club 3")

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
            "approved": True,
        }

        # Create ClubInfo objects
        self.club_info_data_1 = self.base_club_info_data.copy()
        self.club_info_data_1["club"] = self.club_1
        self.club_info_data_1["contact_name"] = "Club 1 contact"
        self.club_info_1 = ClubInfo.objects.create(**self.club_info_data_1)

        self.club_info_data_2 = self.base_club_info_data.copy()
        self.club_info_data_2["club"] = self.club_2
        self.club_info_data_2["contact_name"] = "Club 2 contact"
        self.club_info_data_2["beginners"] = True
        self.club_info_data_2["intermediates"] = True
        self.club_info_data_2["advanced"] = True
        self.club_info_data_2["kids"] = True
        self.club_info_data_2["adults"] = True
        self.club_info_data_2["coaching"] = True
        self.club_info_data_2["league"] = True
        self.club_info_data_2["equipment_provided"] = True
        self.club_info_data_2["membership_required"] = True
        self.club_info_data_2["free_taster"] = True
        self.club_info_2 = ClubInfo.objects.create(**self.club_info_data_2)

        self.club_info_data_3 = self.base_club_info_data.copy()
        self.club_info_data_3["club"] = self.club_3
        self.club_info_data_3["contact_name"] = "Club 3 contact"
        self.club_info_data_3["beginners"] = True
        self.club_info_data_3["intermediates"] = False
        self.club_info_data_3["advanced"] = True
        self.club_info_data_3["kids"] = False
        self.club_info_data_3["adults"] = True
        self.club_info_data_3["coaching"] = False
        self.club_info_data_3["league"] = True
        self.club_info_data_3["equipment_provided"] = False
        self.club_info_data_3["membership_required"] = True
        self.club_info_data_3["free_taster"] = False
        self.club_info_3 = ClubInfo.objects.create(**self.club_info_data_3)

        # Create Venue objects
        self.venue_1 = Venue.objects.create(name="Venue 1")
        self.venue_2 = Venue.objects.create(name="Venue 2")
        self.venue_3 = Venue.objects.create(name="Venue 3")

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
        self.venue_info_data_2["street_address"] = "2 Main Street"
        self.venue_info_2 = VenueInfo.objects.create(**self.venue_info_data_2)

        self.venue_info_data_3 = self.base_venue_info_data.copy()
        self.venue_info_data_3["venue"] = self.venue_3
        self.venue_info_data_3["street_address"] = "3 Main Street"
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

        # Url
        self.url = reverse("clubs")

    def test_no_filters_returns_all_approved_clubs(self):
        """
        Verify all approved clubs are returned when no filters are applied.
        """
        response = self.client.get(self.url)
        self.assertContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_filter_by_beginners_true(self):
        """
        Verify only clubs with beginners=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"beginners": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_filter_by_intermediates_true(self):
        """
        Verify only clubs with intermediates=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"intermediates": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filter_by_advanced_true(self):
        """
        Verify only clubs with advanced=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"advanced": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_filter_by_kids_true(self):
        """
        Verify only clubs with kids=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"kids": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filter_by_adults_true(self):
        """
        Verify only clubs with adults=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"adults": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_filter_by_coaching_true(self):
        """
        Verify only clubs with coaching=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"coaching": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filter_by_league_true(self):
        """
        Verify only clubs with league=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"league": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_filter_by_equipment_provided_true(self):
        """
        Verify only clubs with equipment_provided=True are returned when the
        filter is applied.
        """
        response = self.client.get(self.url, {"equipment_provided": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filter_by_free_taster_true(self):
        """
        Verify only clubs with free_taster=True are returned when the filter
        is applied.
        """
        response = self.client.get(self.url, {"free_taster": "true"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filter_by_membership_required_true(self):
        """
        Verify only clubs with membership_required=True are returned when the
        filter is applied (via dropdown).
        """
        response = self.client.get(self.url, {"membership_required": "True"})
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_filter_by_membership_required_false(self):
        """
        Verify only clubs with membership_required=False are returned when the
        filter is applied (via dropdown).
        """
        response = self.client.get(self.url, {"membership_required": "False"})
        self.assertContains(response, self.club_info_1.contact_name)
        self.assertNotContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filter_by_membership_required_any(self):
        """
        Verify all approved clubs are returned when membership_required is
        unspecified.
        """
        # Should return all approved clubs (like no filter)
        response = self.client.get(self.url, {"membership_required": ""})
        self.assertContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertContains(response, self.club_info_3.contact_name)

    def test_combined_filters(self):
        """
        Verify that multiple filters can be combined to refine results.
        """
        response = self.client.get(
            self.url,
            {
                "beginners": "true",
                "intermediates": "true",
            },
        )
        self.assertNotContains(response, self.club_info_1.contact_name)
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_3.contact_name)

    def test_filters_applied_context_flag(self):
        """
        Verify that the context variable 'filters_applied' is correctly set
        based on the presence of filters.
        """
        # When query params exist, filters_applied should be True
        response = self.client.get(self.url, {"beginners": "true"})
        self.assertTrue(response.context["filters_applied"])

        # When no query params, filters_applied should be False
        response = self.client.get(self.url)
        self.assertFalse(response.context["filters_applied"])

    def test_unapproved_clubs_never_appear_even_if_filter_matches(self):
        """
        Verify unapproved club info entries are excluded from results,
        even if they match the filters.
        """
        self.club_info_1.approved = False
        self.club_info_1.save()
        response = self.client.get(self.url, {"beginners": "true"})
        self.assertNotContains(response, self.club_1.name)

    def test_club_with_no_approved_club_info_does_not_appear(self):
        """
        Verify clubs without any approved club info are excluded from results.
        """
        # Create club without club info
        club_no_info = Club.objects.create(name="No Info Club")
        response = self.client.get(self.url, {"beginners": "true"})
        self.assertNotContains(response, club_no_info.name)

    def test_non_htmx_get_request_loads_whole_page(self):
        """
        Verify that a normal get request loads full clubs page.
        """
        # Simulate an HTMX request filtering by 'beginners'
        response = self.client.get(self.url)

        # Response should include both club_info section and
        # venue_locations section
        self.assertContains(response, 'id="club-info"')
        self.assertContains(response, 'id="venue-locations"')

    def test_htmx_filter_updates_only_club_info_section(self):
        """
        Verify that when the clubs filter is applied via HTMX, only the
        club_info section is updated, while the venue-locations section (map)
        remains unchanged.
        """
        # Simulate an HTMX request filtering by 'beginners'
        response = self.client.get(
            self.url,
            {"beginners": "true"},
            HTTP_HX_REQUEST="true",
        )

        # Response should include club_info section but not
        # venue_locations section
        self.assertContains(response, 'id="club-info"')
        self.assertNotContains(response, 'id="venue-locations"')


class ClubsPageLocationsTests(TestCase):
    def setUp(self):
        """Create clubs, venues and locations data for the tests."""
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

        self.url = reverse("clubs")

    def test_locations_is_in_context(self):
        """
        Verify 'locations' is in the template context.
        """
        response = self.client.get(self.url)
        self.assertIn("locations", response.context)
        self.assertIsInstance(response.context["locations"], list)

    def test_locations_has_correct_structure(self):
        """
        Verify 'locations' has the correct data structure.
        """
        response = self.client.get(self.url)
        locations = response.context["locations"]

        for location in locations:
            self.assertIn("name", location)
            self.assertIn("address", location)
            self.assertIn("lat", location)
            self.assertIn("lng", location)
            self.assertIn("clubs", location)

    def test_locations_only_includes_venues_for_approved_clubs(self):
        """
        Verify 'locations' only includes venues for approved clubs.
        """
        response = self.client.get(self.url)
        locations = response.context["locations"]

        # Extract names from the locations data
        location_names = [loc["name"] for loc in locations]
        self.assertIn(self.venue_1.name, location_names)
        self.assertIn(self.venue_3.name, location_names)
        self.assertNotIn(
            self.venue_2.name, location_names
        )  # Club 2 is unapproved
        self.assertEqual(len(location_names), 2)

    def test_locations_only_includes_approved_venue_info(self):
        """
        Verify 'locations' only includes venues which have approved venue info.
        """
        # Unapprove venue 3
        self.venue_info_3.approved = False
        self.venue_info_3.save()

        response = self.client.get(self.url)
        locations = response.context["locations"]

        # Extract names from the locations data
        location_names = [loc["name"] for loc in locations]
        self.assertEqual(len(location_names), 1)

        # Club 1 has approved club info and approved venue info
        self.assertIn(self.venue_1.name, location_names)

        # Club 3 has approved club info but not venue info
        self.assertNotIn(self.venue_3.name, location_names)

        # Club 2 does not have approved club info
        self.assertNotIn(self.venue_2.name, location_names)

    def test_map_initialises_when_locations_exist(self):
        """
        When 'locations' includes location data
        - the placeholder text 'No locations to display.' should not show.
        - the script for initialising the map should show.
        """
        response = self.client.get(self.url)
        locations = response.context["locations"]

        self.assertGreater(len(locations), 0)
        self.assertNotContains(response, "No locations to display.")
        self.assertContains(response, "initialise_map.js")

    def test_map_when_locations_empty(self):
        """
        When 'locations' is empty
        - the placeholder text 'No locations to display.' should show.
        - the script for initialising the map should not show.
        """
        self.venue_info_1.delete()
        self.venue_info_2.delete()
        self.venue_info_3.delete()

        response = self.client.get(self.url)
        locations = response.context["locations"]

        self.assertEqual(len(locations), 0)
        self.assertContains(response, "No locations to display.")
        self.assertNotContains(response, "initialise_map.js")


class ClubAdminDashboardTests(TestCase):
    """
    Tests for verifying behaviour of the Club Admin Dashboard page.
    """

    def setUp(self):
        """
        Creates user, club, club info, venue info and club admin instances
        for using in tests.
        """
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
    def test_page_displays_for_authenticated_user_with_admin_status(self):
        """
        Verify that the dashboard is accessible for authenticated users
        with club admin status.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/admin_dashboard.html")
        self.assertContains(response, "Club Admin Dashboard")

    def test_page_redirects_unauthenticated_user_to_login_page(self):
        """Verify unauthenticated users are redirected to the login page."""
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_page_redirects_authenticated_user_without_club_admin_status(self):
        """
        Verify that authenticated users without club admin privileges are
        denied access.
        """
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )

    # Club Info
    def test_page_elements_for_missing_club_info(self):
        """Verify that a prompt is shown when club info is missing."""
        self.client.force_login(self.user)
        ClubInfo.objects.all().delete()
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, "Club Information REQUIRED")
        self.assertNotContains(response, "Toggle Preview")

    def test_page_elements_for_unapproved_club_info(self):
        """
        Verify pending approval status prompt is displayed if club info
        has approved=False.
        """
        self.client.force_login(self.user)
        self.club_info_1.approved = False
        self.club_info_1.save()
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, "Club Information (PENDING APPROVAL)")
        self.assertContains(response, "Toggle Preview")
        self.assertContains(response, self.club_info_1.contact_name)

    def test_page_elements_for_approved_club_info(self):
        """
        Verify approved club info is displayed correctly in the dashboard.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, "Club and Venue Information</h2>")
        self.assertContains(response, "Toggle Preview")
        self.assertContains(response, self.club_info_1.contact_name)

    def test_club_info_preview_shows_latest_unapproved_info(self):
        """
        Verify preview section shows the latest unapproved club info
        (if it exists).
        """
        self.client.force_login(self.user)

        # Create new unapproved ClubInfo object
        self.club_info_data_2 = self.base_club_info_data.copy()
        self.club_info_data_2["club"] = self.club
        self.club_info_data_2["contact_name"] = "New Club Contact"
        self.club_info_data_2["approved"] = False
        self.club_info_2 = ClubInfo.objects.create(**self.club_info_data_2)
        self.club_info_2.created_on = timezone.now() + timezone.timedelta(
            minutes=1
        )
        self.club_info_2.save()

        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, self.club_info_2.contact_name)
        self.assertNotContains(response, self.club_info_1.contact_name)

    # Venue Info
    def test_page_elements_for_no_assigned_venues(self):
        """
        Verify prompt is displayed if no venues are assigned to the club.
        """
        self.client.force_login(self.user)
        ClubVenue.objects.all().delete()
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, "Venue REQUIRED")

    def test_page_elements_for_one_assigned_venue(self):
        """
        Verify that the dashboard displays a single assigned venue correctly.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, self.venue_info_1.venue.name)

    def test_page_elements_for_multiple_assigned_venues(self):
        """
        Verify that the dashboard displays all venues assigned to the club.
        """
        self.client.force_login(self.user)

        # Create Second Venue
        self.venue_2 = Venue.objects.create(name="Second Venue Name")

        # Create VenueInfo object
        self.venue_info_data_2 = self.base_venue_info_data.copy()
        self.venue_info_data_2["venue"] = self.venue_2
        self.venue_info_2 = VenueInfo.objects.create(**self.venue_info_data_2)

        # Create ClubVenue object
        self.club_venue = ClubVenue.objects.create(
            club=self.club, venue=self.venue_2
        )

        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, self.venue_info_1.venue.name)
        self.assertContains(response, self.venue_info_2.venue.name)

    def test_page_displays_unapproved_venue(self):
        """
        Verify unapproved venue info is still displayed on the dashboard.
        """
        self.client.force_login(self.user)

        # Unapprove venue
        self.venue_info_1.approved = False
        self.venue_info_1.save()

        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, self.venue_info_1.venue.name)

    def test_page_displays_venue_with_missing_venue_info(self):
        """
        Verify venue without venue info is still listed on the dashboard.
        """
        self.client.force_login(self.user)

        # Create Venue objects
        self.venue_without_info = Venue.objects.create(name="Missing Info")

        # Create ClubVenue object
        self.club_venue = ClubVenue.objects.create(
            club=self.club, venue=self.venue_without_info
        )
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertContains(response, self.venue_without_info.name)


class UpdateClubInfoTests(TestCase):
    """
    Tests for updating club info using the update_club_info view.
    """

    def setUp(self):
        """
        Create user, club, club admin, club info, venue and venue info
        instances for using in tests.
        """
        # Create user and club
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

    # Access Restrictions
    def test_update_club_info_page_displays_for_authenticated_user(self):
        """
        Verify page loads for an authenticated user with club admin status.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("update_club_info"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/update_club_info.html")
        self.assertContains(response, "Update Club Information</h1>")

    def test_page_redirects_unauthenticated_user_to_login_page(self):
        """
        Verify unauthenticated users are redirected to the login page.
        """
        response = self.client.get(reverse("update_club_info"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_page_redirects_authenticated_user_without_club_admin_status(self):
        """
        Verify authenticated users without admin status receive a
        403 Forbidden error.
        """
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(reverse("update_club_info"))
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )

    # Test form rendering for GET request
    def test_update_club_info_page_renders_form(self):
        """
        Verify form is rendered correctly on GET request for authorised users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("update_club_info"))
        self.assertContains(response, '<input type="text"')
        self.assertContains(response, "<label")
        self.assertContains(response, "Club Website")  # A label
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], UpdateClubInfoForm)

    def test_page_contains_csrf(self):
        """
        Verify presence of CSRF token.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("update_club_info"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_update_club_info_form_prefills_latest_club_info_data(self):
        """
        Verify form pre-fills with the latest club info data.
        """
        self.client.force_login(self.user)

        # Create Newer ClubInfo object
        self.new_club_info_data = {
            "club": self.club,
            "image": "",
            "website": "https://www.newexample.com",
            "contact_name": "New Contact Name",
            "contact_email": "newexample@newexample.com",
            "contact_phone": "01234566666",
            "description": "This club is new!",
            "session_info": "We start soon.",
            "beginners": True,
            "approved": False,
        }
        self.new_club_info = ClubInfo.objects.create(**self.new_club_info_data)
        self.new_club_info.created_on = timezone.now() + timezone.timedelta(
            minutes=1
        )
        self.new_club_info.save()

        # Check most recent data is prefilled
        response = self.client.get(reverse("update_club_info"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["website"],
            self.new_club_info.website,
        )
        self.assertEqual(
            response.context["form"].initial["contact_name"],
            self.new_club_info.contact_name,
        )
        self.assertEqual(
            response.context["form"].initial["contact_email"],
            self.new_club_info.contact_email,
        )
        self.assertEqual(
            response.context["form"].initial["contact_phone"],
            self.new_club_info.contact_phone,
        )
        self.assertEqual(
            response.context["form"].initial["description"],
            self.new_club_info.description,
        )
        self.assertEqual(
            response.context["form"].initial["session_info"],
            self.new_club_info.session_info,
        )
        self.assertEqual(
            response.context["form"].initial["beginners"],
            self.new_club_info.beginners,
        )

    def test_update_club_info_form_renders_when_no_previous_club_info_data(
        self,
    ):
        """
        Verify form renders without errors when no prior club info exists.
        """
        self.client.force_login(self.user)

        # Delete ClubInfo records
        ClubInfo.objects.all().delete()

        # Check form renders without prefilled data
        response = self.client.get(reverse("update_club_info"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("club", response.context["form"].initial)
        self.assertNotIn("contact_name", response.context["form"].initial)

    # Test form submissions with POST request
    def test_authenticated_user_can_submit_valid_update_club_info_form(self):
        """
        Verify valid form submission by an authorised user creates a new
        ClubInfo and shows a success message.
        """
        self.client.force_login(self.user)
        form_data = {
            "image": "",
            "website": "https://www.newexample.com",
            "contact_name": "New Contact Name",
            "contact_email": "newexample@example.com",
            "contact_phone": "01234555555",
            "description": "This club info is new!",
            "session_info": "We will do many nights.",
        }
        response = self.client.post(
            reverse("update_club_info"), form_data, follow=True
        )
        self.assertRedirects(response, reverse("club_admin_dashboard"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Club info has been updated.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

        # Check database entry
        club_info = ClubInfo.objects.get(
            contact_name=form_data["contact_name"]
        )
        self.assertEqual(club_info.club, self.club)
        self.assertEqual(club_info.website, form_data["website"])
        self.assertEqual(club_info.contact_name, form_data["contact_name"])
        self.assertEqual(club_info.contact_email, form_data["contact_email"])
        self.assertEqual(club_info.contact_phone, form_data["contact_phone"])
        self.assertEqual(club_info.description, form_data["description"])
        self.assertEqual(club_info.session_info, form_data["session_info"])

    def test_unauthenticated_user_cannot_submit_form(self):
        """
        Verify unauthenticated users cannot submit the form and are redirected
        to login page.
        """
        form_data = {
            "image": "",
            "website": "https://www.newexample.com",
            "contact_name": "New Contact Name",
            "contact_email": "newexample@example.com",
            "contact_phone": "01234555555",
            "description": "This club info is new!",
            "session_info": "We will do many nights.",
        }
        response = self.client.post(
            reverse("update_club_info"), form_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                "/accounts/login/" in url for url, _ in response.redirect_chain
            )
        )

        # Check database entry
        self.assertEqual(ClubInfo.objects.count(), 1)
        self.assertEqual(
            ClubInfo.objects.filter(
                contact_name=form_data["contact_name"]
            ).count(),
            0,
        )

    def test_club_info_record_cleanup_after_valid_form_submission(self):
        """
        Verify only latest approved and submitted ClubInfo records remain
        after a new submission.
        """
        self.client.force_login(self.user)

        # Create Another approved ClubInfo object
        self.club_info_data_2 = self.base_club_info_data.copy()
        self.club_info_data_2["club"] = self.club
        self.club_info_data_2["contact_name"] = "Approved Contact 2"
        self.club_info_2 = ClubInfo.objects.create(**self.club_info_data_2)
        self.club_info_2.created_on = timezone.now() + timezone.timedelta(
            minutes=1
        )
        self.club_info_2.save()

        # Create unapproved ClubInfo object
        self.club_info_data_3 = self.base_club_info_data.copy()
        self.club_info_data_3["club"] = self.club
        self.club_info_data_3["contact_name"] = "Unapproved Contact 3"
        self.club_info_data_3["approved"] = False
        self.club_info_3 = ClubInfo.objects.create(**self.club_info_data_3)
        self.club_info_3.created_on = timezone.now() + timezone.timedelta(
            minutes=2
        )
        self.club_info_3.save()

        form_data = {
            "image": "",
            "website": "https://www.newexample.com",
            "contact_name": "New Contact Name",
            "contact_email": "newexample@example.com",
            "contact_phone": "01234555555",
            "description": "This club info is new!",
            "session_info": "We will do many nights.",
        }
        response = self.client.post(
            reverse("update_club_info"), form_data, follow=True
        )
        self.assertRedirects(response, reverse("club_admin_dashboard"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Club info has been updated.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

        # Check database entry
        # It should contain latest approved and newly submitted records only
        self.assertEqual(ClubInfo.objects.count(), 2)
        self.assertEqual(
            ClubInfo.objects.filter(
                contact_name=form_data["contact_name"]
            ).count(),
            1,
            msg="ClubInfo record for new form submission should exist",
        )
        self.assertEqual(
            ClubInfo.objects.filter(id=self.club_info_2.id).count(),
            1,
            msg="Latest approved ClubInfo record should exist",
        )
        self.assertEqual(
            ClubInfo.objects.filter(id=self.club_info_1.id).count(),
            0,
            msg="Early approved ClubInfo record should no longer exist",
        )
        self.assertEqual(
            ClubInfo.objects.filter(id=self.club_info_3.id).count(),
            0,
            msg="Early unapproved ClubInfo record should no longer exist",
        )

    # Test Invalid form submissions
    def test_invalid_form_submission_shows_warning(self):
        """
        Verify submitting invalid form data shows field-specific errors and
        a warning message.
        """
        self.client.force_login(self.user)
        form_data = {
            "image": "",
            "website": "",
            "contact_name": "",
            "contact_email": "not.an.email",
            "contact_phone": "123",
            "description": "",
            "session_info": "",
        }
        response = self.client.post(
            reverse("update_club_info"), form_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "contact_name", "This field is required."
        )
        self.assertFormError(
            response, "form", "contact_email", "Enter a valid email address."
        )
        self.assertContains(response, "Form data was invalid")

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Form data was invalid - please check the error message(s)",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.WARNING)


class DeleteClubInfoTests(TestCase):
    """
    Tests club information deletion using the delete_club_info view.
    """

    def setUp(self):
        """
        Create user, club, club admin, and initial ClubInfo records
        (approved and unapproved) for use in tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")

        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

        self.club_info_approved = ClubInfo.objects.create(
            club=self.club,
            website="",
            contact_name="Approved Contact",
            contact_email="approved@example.com",
            contact_phone="01234567888",
            description="Approved club info",
            session_info="Approved session info",
            approved=True,
        )
        self.club_info_unapproved = ClubInfo.objects.create(
            club=self.club,
            website="",
            contact_name="Unapproved Contact",
            contact_email="unapproved@example.com",
            contact_phone="01234567888",
            description="Unapproved club info",
            session_info="Unapproved session info",
            approved=False,
        )

    # Access restriction tests
    def test_page_redirects_unauthenticated_user(self):
        """
        Verify unauthenticated users are redirected to login page when
        attempt to access the delete page.
        """
        response = self.client.get(reverse("delete_club_info"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_page_restricts_non_club_admin_user(self):
        """
        Verify users without club admin status receive a 403 Forbidden error.
        """
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))
        self.assertEqual(response.status_code, 403)

    def test_delete_club_info_renders_on_get(self):
        """
        Verify the delete confirmation page renders correctly on GET request
        for authorised users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "clubs/confirm_delete_club_info.html"
        )

    # Check page elements exist
    def test_delete_club_info_has_heading_and_warning(self):
        """
        Verify page includes heading and warning text.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))

        self.assertContains(response, "Delete Club Information</h1>")
        self.assertContains(
            response, "Deleting club information cannot be undone."
        )
        self.assertContains(response, "href=")

    def test_delete_club_info_form_has_crsf_token(self):
        """
        Verify the delete club info form is rendered with a CSRF token.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))

        self.assertContains(response, "<form")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_delete_club_info_has_radio_buttons(self):
        """
        Verify the form contains the correct radio buttons for delete options.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))

        self.assertContains(response, "Choose what to delete:")
        self.assertContains(response, 'type="radio"')
        self.assertContains(response, 'name="delete_option"')
        self.assertContains(response, 'value="all"')
        self.assertContains(response, 'value="unapproved"')

    def test_delete_club_info_has_confirmation_checkbox(self):
        """
        Verify the form includes a required confirmation checkbox.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))

        self.assertContains(response, 'type="checkbox"')
        self.assertContains(
            response,
            "I understand that this will cause the club to disappear"
            " from the Clubs page",
        )

    def test_delete_club_info_has_buttons(self):
        """
        Verify the form includes Delete and Cancel buttons.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_club_info"))

        self.assertContains(response, "Delete Club Info</button>")
        self.assertContains(response, "Cancel</a>")

    # Test DELETE ALL behaviour
    def test_delete_all_with_confirmation_checkbox_checked(self):
        """
        Verify all ClubInfo records are deleted when 'all' is selected
        and confirmation checkbox is checked.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("delete_club_info"),
            {"delete_option": "all", "confirm_action": "on"},
            follow=True,
        )
        self.assertRedirects(response, reverse("club_admin_dashboard"))
        self.assertEqual(ClubInfo.objects.filter(club=self.club).count(), 0)
        msgs = list(response.context["messages"])
        self.assertEqual(msgs[0].level, messages.SUCCESS)
        self.assertIn("Club info has been deleted.", msgs[0].message)

    def test_delete_all_without_confirmation_checkbox_shows_warning(self):
        """
        Verify warning is shown if 'all' is selected but confirmation checkbox
        is not checked.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("delete_club_info"),
            {"delete_option": "all"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please tick the confirmation checkbox")
        self.assertEqual(ClubInfo.objects.filter(club=self.club).count(), 2)

    # Test DELETE UNAPPROVED behaviour
    def test_delete_unapproved_only(self):
        """
        Verify only unapproved ClubInfo records are deleted when 'unapproved'
        is selected.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("delete_club_info"),
            {"delete_option": "unapproved"},
            follow=True,
        )
        self.assertRedirects(response, reverse("club_admin_dashboard"))
        self.assertEqual(ClubInfo.objects.filter(club=self.club).count(), 1)
        self.assertTrue(
            ClubInfo.objects.filter(id=self.club_info_approved.id).exists()
        )
        msgs = list(response.context["messages"])
        self.assertEqual(msgs[0].level, messages.SUCCESS)
        self.assertIn(
            "Unapproved club info has been deleted.", msgs[0].message
        )

    def test_delete_unapproved_when_none_exist_shows_warning(self):
        """
        Verify warning is shown if there are no unapproved records to delete.
        """
        self.client.force_login(self.user)
        self.club_info_unapproved.delete()
        response = self.client.post(
            reverse("delete_club_info"),
            {"delete_option": "unapproved"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context["messages"])
        self.assertEqual(msgs[0].level, messages.WARNING)
        self.assertIn(
            "There is no unapproved club information", msgs[0].message
        )
        self.assertEqual(ClubInfo.objects.filter(club=self.club).count(), 1)

    # Test invalid option
    def test_invalid_delete_option_shows_warning(self):
        """
        Verify warning is shown when an invalid delete option is submitted.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("delete_club_info"),
            {"delete_option": "invalid_option"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context["messages"])
        self.assertEqual(msgs[0].level, messages.WARNING)
        self.assertIn("An error occurred.", msgs[0].message)
        self.assertEqual(ClubInfo.objects.filter(club=self.club).count(), 2)


class UnassignVenueViewTests(TestCase):
    """
    Tests for unassigning a venue from a club using the unassign_venue view.
    """

    def setUp(self):
        """
        Create user, club, club admin, venue and club venue records for using
        in tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")
        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

        self.venue = Venue.objects.create(name="Test Venue")
        self.club_venue = ClubVenue.objects.create(
            club=self.club, venue=self.venue
        )

        self.url = reverse("unassign_venue", args=[self.venue.id])

    # Access restriction tests
    def test_redirects_unauthenticated_user(self):
        """Verify unauthenticated users are redirected to the login page."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_forbids_non_club_admin_user(self):
        """
        Verify access is forbidden for authenticated users without club admin
        status.
        """
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_rejects_get_request(self):
        """Verify GET requests are rejected with a 403 status."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    # Valid POST request behaviour
    def test_successfully_unassigns_venue(self):
        """
        Verify POST successfully unassigns a venue for an authorised user.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "clubs/partials/admin_club_info_section.html"
        )
        self.assertFalse(
            ClubVenue.objects.filter(club=self.club, venue=self.venue).exists()
        )

    def test_post_when_venue_not_assigned_does_not_error(self):
        """Verify POST does not error when the venue is already unassigned."""
        self.club_venue.delete()
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "clubs/partials/admin_club_info_section.html"
        )

    def test_post_with_nonexistent_venue_does_not_error(self):
        """
        Verify POST with a nonexistent venue id does not result in an error.
        """
        self.client.force_login(self.user)
        url = reverse("unassign_venue", args=[9999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "clubs/partials/admin_club_info_section.html"
        )


class AssignVenueTests(TestCase):
    """
    Tests for assigning venues to clubs using the assign_venue view.
    """

    def setUp(self):
        """
        Create user, club, club admin and venue records ready for assigning
        venues to clubs.
        """
        # Create user and club
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")
        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

        # Create venue
        self.venue = Venue.objects.create(name="Venue 1")

        # Assign URL
        self.url = reverse("assign_venue")

    # Access restriction tests
    def test_redirects_unauthenticated_user(self):
        """Verify unauthenticated users are redirected to the login page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_forbids_user_without_club_admin_status(self):
        """Verify users without club admin status cannot access the view."""
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    # GET requests
    def test_get_request_renders_form_with_available_venues(self):
        """Verify GET renders the form with available venues for assignment."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/assign_venue.html")
        self.assertContains(response, "Assign Venue</h1>")
        self.assertIn("form", response.context)
        self.assertFalse(response.context["no_available_venues"])

    def test_get_request_when_no_available_venues(self):
        """Verify prompt when no venues are available to assign."""
        self.client.force_login(self.user)

        # Make venue assigned to club already
        ClubVenue.objects.create(club=self.club, venue=self.venue)
        response = self.client.get(self.url)

        # Check context
        self.assertTrue(response.context["no_available_venues"])

        # Check page rendering
        self.assertContains(
            response, "There are no available venues to assign."
        )
        self.assertContains(response, "Cancel</a>")

    def test_get_request_contains_csrf_token(self):
        """Verify CSRF token is present in the rendered form."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    # POST (valid)
    def test_valid_post_assigns_venue_to_club(self):
        """
        Verify valid form submission assigns a venue and displays a
        success message.
        """
        self.client.force_login(self.user)
        form_data = {"venue": self.venue.id}
        response = self.client.post(self.url, data=form_data, follow=True)
        self.assertRedirects(response, reverse("club_admin_dashboard"))

        self.assertTrue(
            ClubVenue.objects.filter(club=self.club, venue=self.venue).exists()
        )

        msgs = list(response.context["messages"])
        self.assertEqual(msgs[0].message, "Venue has been assigned.")
        self.assertEqual(msgs[0].level, messages.SUCCESS)

    # POST (invalid)
    def test_invalid_post_data_rerenders_form(self):
        """Verify form is rendered with errors when data is invalid."""
        self.client.force_login(self.user)
        form_data = {"venue": ""}  # Empty is invalid
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "venue", "This field is required."
        )

    def test_post_with_invalid_venue_id_shows_form_error(self):
        """Verify form displays appropriate error for an invalid venue ID."""
        self.client.force_login(self.user)
        form_data = {"venue": 999}  # Invalid ID
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "venue",
            (
                "Select a valid choice."
                " That choice is not one of the available choices."
            ),
        )

    def test_venue_becomes_unavailable_before_form_submission(self):
        """Verify error message is shown if venue becomes unavailable after
        form load."""
        self.client.force_login(self.user)

        # Render form (GET request)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn(self.venue, form.fields["venue"].queryset)

        # Simulate another user assigning the venue before form is submitted
        ClubVenue.objects.create(club=self.club, venue=self.venue)

        # Attempt to submit form with now unavailable venue
        form_data = {"venue": self.venue.id}
        response = self.client.post(self.url, form_data)

        # Check warning message
        self.assertEqual(response.status_code, 200)
        msgs = list(response.context["messages"])
        self.assertIn("Something went wrong.", msgs[0].message)
        self.assertEqual(msgs[0].level, messages.WARNING)

        # Check that the venue is still only assigned once
        self.assertEqual(
            ClubVenue.objects.filter(club=self.club, venue=self.venue).count(),
            1,
        )


class UpdateVenueInfoTests(TestCase):
    def setUp(self):
        """
        Create user, club, club admin, venue, venue info and club venue
        records ready forupdating venue information.
        """
        # Create user and club
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")

        # Assign ClubAdmin
        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

        # Create Venue and link to club
        self.venue = Venue.objects.create(name="Test Venue")
        self.club_venue = ClubVenue.objects.create(
            club=self.club, venue=self.venue
        )

        # Base VenueInfo data
        self.base_venue_info_data = {
            "venue": self.venue,
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
        self.venue_info = VenueInfo.objects.create(**self.base_venue_info_data)

        self.url = reverse("update_venue_info", args=[self.venue.id])

    # Access Restrictions
    def test_page_displays_for_authenticated_club_admin(self):
        """
        Verify authenticated club admin can access the update page.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/update_venue_info.html")
        self.assertContains(response, "Update Venue Information")

    def test_redirects_unauthenticated_user_to_login_page(self):
        """Verify unauthenticated users are redirected to login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_rejects_authenticated_user_without_club_admin_status(self):
        """Verify that non-admin users receive a 403 on access attempt."""
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )

    def test_rejects_club_admin_not_associated_with_venue(self):
        """Verify admins not linked to the venue are redirected."""
        other_venue = Venue.objects.create(name="Other Venue")
        other_url = reverse("update_venue_info", args=[other_venue.id])
        self.client.force_login(self.user)
        response = self.client.get(other_url)
        self.assertRedirects(response, reverse("club_admin_dashboard"))

    # GET request and form rendering
    def test_update_venue_info_form_prefills_latest_venue_info_data(self):
        """Verify form is prefilled with the latest VenueInfo data."""
        self.client.force_login(self.user)

        new_info_data = self.base_venue_info_data.copy()
        new_info_data["street_address"] = "123 New Street"
        new_info_data["city"] = "New City"
        new_info = VenueInfo.objects.create(**new_info_data)
        new_info.created_on = timezone.now() + timezone.timedelta(minutes=1)
        new_info.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["street_address"],
            "123 New Street",
        )
        self.assertEqual(response.context["form"].initial["city"], "New City")

    def test_update_venue_info_form_renders_when_no_previous_data(self):
        """Verify form renders correctly when no prior VenueInfo exists."""
        self.client.force_login(self.user)
        VenueInfo.objects.all().delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertNotIn("street_address", response.context["form"].initial)

    def test_csrf_token_is_present_in_form(self):
        """Verify that the CSRF token is included in the form."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    # POST request - Valid submission
    def test_club_admin_can_submit_valid_form(self):
        """
        Verify valid form submission creates a new VenueInfo and redirects.
        """
        ...
        self.client.force_login(self.user)
        form_data = {
            "street_address": "45 New Road",
            "address_line_2": "Apartment 2",
            "city": "Newcastle",
            "county": "Tyne and Wear",
            "postcode": "NE1 1AA",
            "num_tables": 6,
            "parking_info": "Underground parking",
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(response, reverse("club_admin_dashboard"))

        # Message test
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertIn("Venue info has been updated", messages_list[0].message)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

        # Database entry test
        self.assertTrue(
            VenueInfo.objects.filter(
                venue=self.venue,
                street_address="45 New Road",
                city="Newcastle",
            ).exists()
        )

    def test_previous_venue_info_cleanup_after_submission(self):
        """
        Verify outdated VenueInfo entries are removed after creating
        a new venue info record.
        """
        self.client.force_login(self.user)

        # Create another older record
        old_info = VenueInfo.objects.create(
            **{**self.base_venue_info_data, "street_address": "Old Address"}
        )
        old_info.created_on = timezone.now() - timezone.timedelta(minutes=1)
        old_info.save()

        form_data = {
            "street_address": "New Address",
            "address_line_2": "",
            "city": "Leeds",
            "county": "West Yorkshire",
            "postcode": "LS1 4AB",
            "num_tables": 12,
            "parking_info": "Free street parking",
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertRedirects(response, reverse("club_admin_dashboard"))

        venue_infos = VenueInfo.objects.filter(venue=self.venue)
        self.assertEqual(venue_infos.count(), 2)
        self.assertTrue(
            venue_infos.filter(street_address="New Address").exists()
        )

    # POST request - Invalid submission
    def test_invalid_form_submission_shows_warning_and_errors(self):
        """
        Verify form errors and warnings are shown for invalid submissions.
        """
        self.client.force_login(self.user)
        form_data = {
            "street_address": "",
            "city": "Invalid City",
            "county": "County",
            "postcode": "",
            "num_tables": "",
            "parking_info": "",
        }
        response = self.client.post(self.url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "street_address", "This field is required."
        )
        self.assertFormError(
            response, "form", "postcode", "This field is required."
        )
        self.assertFormError(
            response, "form", "num_tables", "This field is required."
        )

        # Check warning message
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertIn(
            "Please correct the highlighted errors", messages_list[0].message
        )
        self.assertEqual(messages_list[0].level, messages.WARNING)

    # Shared Venue Tests
    def test_shared_venues_message_displays_for_shared_venue(self):
        """
        Verify shared venue message appears when venue is linked to
        multiple clubs.
        """
        self.client.force_login(self.user)

        # Create another club which shares the venue
        club_2 = Club.objects.create(name="Club 2")
        ClubVenue.objects.create(club=club_2, venue=self.venue)

        response = self.client.get(self.url)
        self.assertIn(
            "is_shared_venue",
            response.context,
            msg="is_shared_venue not found as a context variable",
        )
        self.assertTrue(response.context["is_shared_venue"])
        self.assertContains(response, "This venue is shared with other clubs.")

    def test_shared_venues_message_not_displayed_for_non_shared_venue(self):
        """
        Verify shared venue message is absent when venue is not shared.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertIn(
            "is_shared_venue",
            response.context,
            msg="is_shared_venue not found as a context variable",
        )
        self.assertFalse(response.context["is_shared_venue"])
        self.assertNotContains(
            response, "This venue is shared with other clubs."
        )


class CreateVenueTests(TestCase):
    """Tests for creating a venue using the create_venue view."""

    def setUp(self):
        """
        Set up user, club, club admin records and initial venue info data
        for use in the tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")

        # Grant club admin status
        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

        self.valid_venue_data = {
            "name": "New Venue",
        }

        self.valid_venue_info_data = {
            "street_address": "123 Street",
            "address_line_2": "",
            "city": "York",
            "county": "Yorkshire",
            "postcode": "YO1 1AA",
            "num_tables": 5,
            "parking_info": "Parking is available nearby.",
        }

        self.url = reverse("create_venue")

    # Access Restrictions
    def test_redirects_unauthenticated_user(self):
        """Verify unauthenticated users are redirected to the login page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_redirects_user_without_club_admin_status(self):
        """
        Verify users without club admin status receive a 403 permission error.
        """
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )

    def test_authenticated_club_admin_can_view_page(self):
        """
        Verify authenticated club admins can access the create venue page.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/create_venue.html")
        self.assertContains(response, "Create Venue")

    def test_page_contains_csrf_token(self):
        """Verify CSRF token is present."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    # Form Submission
    def test_valid_post_creates_venue_and_info(self):
        """
        Verify valid form submission creates venue and associated info objects.
        """
        self.client.force_login(self.user)
        post_data = {**self.valid_venue_data, **self.valid_venue_info_data}

        response = self.client.post(self.url, post_data, follow=True)

        self.assertRedirects(response, reverse("club_admin_dashboard"))
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertIn("Venue has been created", messages_list[0].message)

        # Check Database objects
        venue = Venue.objects.get(name=self.valid_venue_data["name"])
        venue_info = VenueInfo.objects.get(venue=venue)
        self.assertEqual(
            venue_info.street_address,
            self.valid_venue_info_data["street_address"],
        )

    def test_invalid_post_does_not_create_objects(self):
        """
        Verify form errors prevent venue and info creation when invalid data
        is submitted.
        """
        self.client.force_login(self.user)
        invalid_data = {
            "name": "",  # Invalidates venue form
            "street_address": "",  # Invalidates venue_info form
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response, "venue_form", "name", "This field is required."
        )
        self.assertFormError(
            response,
            "venue_info_form",
            "street_address",
            "This field is required.",
        )
        self.assertEqual(Venue.objects.count(), 0)
        self.assertEqual(VenueInfo.objects.count(), 0)

    def test_duplicate_venue_name_shows_error(self):
        """
        Verify error is shown when attempting to create a venue with
        a duplicate name.
        """
        self.client.force_login(self.user)
        Venue.objects.create(name="New Venue")

        post_data = {**self.valid_venue_data, **self.valid_venue_info_data}
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "venue_form",
            "name",
            "Venue with this Name already exists.",
        )
        self.assertEqual(Venue.objects.count(), 1)
        self.assertEqual(VenueInfo.objects.count(), 0)


class DeleteVenueTests(TestCase):
    """Tests for deleting venue functionality using the delete_venue view."""

    def setUp(self):
        """Create user, club, club admin, venue and club venue records
        ready for the deletion tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.club = Club.objects.create(name="Test Club")
        self.club_admin = ClubAdmin.objects.create(
            user=self.user, club=self.club
        )

        self.venue = Venue.objects.create(name="Test Venue")
        self.club_venue = ClubVenue.objects.create(
            club=self.club, venue=self.venue
        )

        self.url = reverse("delete_venue", args=[self.venue.id])

    # Access Restrictions
    def test_redirects_unauthenticated_user(self):
        """
        Verify unauthenticated users are redirected to login page when
        accessing venue deletion confirmation page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_redirects_user_without_club_admin_status(self):
        """
        Verify non-admin users are denied access to venue deletion
        confirmation page.
        """
        self.club_admin.delete()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )

    def test_authenticated_club_admin_can_view_page(self):
        """
        Verify club admin can access the venue deletion confirmation page.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clubs/confirm_delete_venue.html")
        self.assertContains(response, "Delete Venue")

    # GET Page Rendering
    def test_shared_venue_notification_displays_when_venue_is_shared(self):
        """
        Verify shared venue warning is shown when venue is used by multiple
        clubs.
        """
        self.client.force_login(self.user)

        # Create club which shares venue
        sharing_club = Club.objects.create(name="Sharing Club")
        ClubVenue.objects.create(club=sharing_club, venue=self.venue)

        response = self.client.get(self.url)
        self.assertContains(response, "This venue is shared with other clubs.")

    def test_shared_venue_notification_not_displayed_when_venue_not_shared(
        self,
    ):
        """
        Verify no warning appears if the venue is not shared with other clubs.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertNotContains(
            response, "This venue is shared with other clubs."
        )

    # POST Logic - Unapproved Info Only
    def test_delete_unapproved_info_only(self):
        """Verify only unapproved venue info is deleted when selected."""
        self.client.force_login(self.user)
        unapproved_info = VenueInfo.objects.create(
            venue=self.venue,
            street_address="123",
            city="York",
            county="Yorkshire",
            postcode="YO1 1AA",
            num_tables=4,
            parking_info="None",
            approved=False,
        )
        post_data = {"delete_option": "unapproved"}
        response = self.client.post(self.url, post_data, follow=True)

        self.assertRedirects(response, reverse("club_admin_dashboard"))

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual(
            "Unapproved venue info has been deleted.", messages_list[0].message
        )

        self.assertFalse(
            VenueInfo.objects.filter(id=unapproved_info.id).exists()
        )

    def test_delete_unapproved_info_shows_warning_when_none_exist(self):
        """
        Verify warning message is shown if no unapproved venue info exists
        to delete.
        """
        self.client.force_login(self.user)
        post_data = {"delete_option": "unapproved"}
        response = self.client.post(self.url, post_data, follow=True)

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)
        self.assertEqual(
            "There is no unapproved venue information to delete.",
            messages_list[0].message,
        )

    # POST Logic - Delete Venue
    def test_delete_venue_with_checkbox_checked(self):
        """
        Verify venue is deleted when 'delete all' is selected and confirmed.
        """
        self.client.force_login(self.user)
        post_data = {
            "delete_option": "all",
            "confirm_action": "on",
        }
        response = self.client.post(self.url, post_data, follow=True)

        self.assertRedirects(response, reverse("club_admin_dashboard"))

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertEqual("Venue has been deleted.", messages_list[0].message)

        self.assertFalse(Venue.objects.filter(id=self.venue.id).exists())

    def test_cannot_delete_venue_if_shared(self):
        """Verify venue cannot be deleted if it is shared with other clubs."""
        sharing_club = Club.objects.create(name="Sharing Club")
        ClubVenue.objects.create(club=sharing_club, venue=self.venue)
        self.client.force_login(self.user)

        post_data = {
            "delete_option": "all",
            "confirm_action": "on",
        }
        response = self.client.post(self.url, post_data)

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)
        self.assertIn(
            "Cannot delete venue because it is shared",
            messages_list[0].message,
        )

        self.assertTrue(Venue.objects.filter(id=self.venue.id).exists())

    def test_delete_venue_requires_checkbox_confirmation(self):
        """Verify checkbox confirmation is required to delete venue."""
        self.client.force_login(self.user)
        post_data = {"delete_option": "all"}  # checkbox omitted
        response = self.client.post(self.url, post_data, follow=True)

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)
        self.assertIn(
            "Please tick the confirmation checkbox", messages_list[0].message
        )

        self.assertTrue(Venue.objects.filter(id=self.venue.id).exists())

    def test_invalid_post_option_returns_error_message(self):
        """Verify invalid delete option returns appropriate error message."""
        self.client.force_login(self.user)
        post_data = {"delete_option": "invalid"}
        response = self.client.post(self.url, post_data, follow=True)

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)
        self.assertIn("An error occurred", messages_list[0].message)

    def test_redirect_if_venue_does_not_exist(self):
        """Verify user is redirected if venue does not exist."""
        self.client.force_login(self.user)
        invalid_url = reverse("delete_venue", args=[999])
        response = self.client.get(invalid_url, follow=True)

        self.assertRedirects(response, reverse("club_admin_dashboard"))

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)
        self.assertIn("Unable to delete venue.", messages_list[0].message)

    def test_redirect_if_venue_not_assigned_to_club(self):
        """
        Verify user is redirected if venue is not assigned to user's club.
        """
        other_venue = Venue.objects.create(name="Other Venue")
        other_url = reverse("delete_venue", args=[other_venue.id])
        self.client.force_login(self.user)
        response = self.client.get(other_url, follow=True)

        self.assertRedirects(response, reverse("club_admin_dashboard"))

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.WARNING)
        self.assertIn("Unable to delete venue.", messages_list[0].message)
