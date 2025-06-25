from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from home.models import NewsItem


class HomePageStaticTests(TestCase):
    """
    Unit tests for the home page to verify status code, template usage,
    and presence of key static content sections and elements.
    """
    def test_homepage_returns_correct_status_code(self):
        """
        Verify home page responds with HTTP 200 OK status.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_returns_correct_template(self):
        """
        Verify home page uses the expected template.
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/home.html")

    def test_homepage_has_hidden_title(self):
        """
        Verify home page contains a visually hidden <h1> element
        with the site title for accessibility.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<h1 class="visually-hidden"')
        self.assertContains(response, "City and District Table Tennis League")

    # Hero Section
    def test_homepage_contains_hero_section(self):
        """
        Verify home page contains hero section element.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'id="hero"')

    def test_homepage_contains_hero_image(self):
        """
        Verify hero section includes webp image with jpg fallback
        and correct alt text.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<picture>")
        self.assertContains(response, 'srcset="/static/images/hero.webp"')
        self.assertContains(response, 'srcset="/static/images/hero.jpg"')
        self.assertContains(response, "<img")
        self.assertContains(
            response, 'alt="Action shot of table tennis player in an arena"'
        )

    def test_homepage_contains_hero_overlay(self):
        """
        Verify presence of hero overlay image with correct src and alt
        attributes.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'id="hero-overlay"')
        self.assertContains(response, 'src="/static/images/hero-overlay.png"')
        self.assertContains(
            response, 'alt="City and District Table Tennis League Logo"'
        )

    # About Section
    def test_homepage_contains_about_section(self):
        """
        Verify about section exists and contains expected introduction.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="about"')
        self.assertContains(
            response, "Welcome to the City and District Table Tennis League!"
        )
        self.assertContains(response, "Founded in 2015")

    # News Section
    def test_homepage_contains_news_section(self):
        """
        Verify news section exists and contains visually hidden heading
        "Latest News".
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="news"')
        self.assertContains(response, "Latest News")

    # FAQ Section
    def test_homepage_contains_useful_links_section(self):
        """
        Verify Useful Links section contains heading and card titles for
        navigating to Clubs, League Tables, Fixtures and Results pages.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="useful-links"')
        self.assertContains(response, "Useful Links</h2>")
        self.assertContains(response, "card-title")
        self.assertContains(response, "Find a Club</h3>")
        self.assertContains(response, "League Tables</h3>")
        self.assertContains(response, "Fixtures</h3>")
        self.assertContains(response, "Results</h3>")

    # FAQ Section
    def test_homepage_contains_faq_section(self):
        """
        Verify FAQ section contains the expected introductory text,
        accordion elements and at least one question.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="faq"')
        self.assertContains(
            response,
            "Find answers to the most frequently asked questions",
        )
        self.assertContains(response, 'id="accordion-faq"')
        self.assertContains(response, 'class="accordion-item')
        self.assertContains(response, "Who can join the league?")

    # Sponsors Section
    def test_homepage_contains_sponsors_section(self):
        """
        Verify sponsors section contains the heading and sponsor images
        with expected classes and attributes.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="sponsors"')
        self.assertContains(response, "League Sponsors")
        self.assertContains(response, 'class="sponsor-img"')
        self.assertContains(response, 'rel="noopener noreferrer"')

    # Footer Section
    def test_homepage_contains_footer(self):
        """
        Verify the footer contains contact section, social media icons,
        and copyright text.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<footer")
        self.assertContains(response, '<section id="contact"')
        self.assertContains(response, 'class="social-media"')
        self.assertContains(response, "fa-brands fa-instagram")
        self.assertContains(response, "fa-brands fa-square-facebook")
        self.assertContains(response, "fa-brands fa-x-twitter")
        self.assertContains(response, "© 2025 Peter Lowry")


class HomePageDynamicNewsTests(TestCase):
    """
    Tests for the dynamic news section on the home page, verifying
    placeholder display when no news exist, correct filtering of
    active news items and carousel navigation button visibility.
    """
    def test_homepage_displays_placeholder_when_no_news_items(self):
        """
        Verify that when no news items are available, the home page shows
        a placeholder message and hides the news carousel.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No news items to show at the moment.")
        self.assertNotContains(response, 'id="news-carousel"')

    def test_homepage_displays_only_active_news_items(self):
        """
        Verify that only currently active news items are displayed on the
        home page and that future and expired news items are excluded.
        """
        # Add news items
        now = timezone.now()
        active_news = NewsItem.objects.create(
            title="Active News",
            content="This is active",
            active_from=now - timezone.timedelta(days=1),
            active_to=now + timezone.timedelta(days=1),
        )
        future_news = NewsItem.objects.create(
            title="Future News",
            content="Not yet active",
            active_from=now + timezone.timedelta(days=1),
            active_to=now + timezone.timedelta(days=2),
        )
        expired_news = NewsItem.objects.create(
            title="Expired News",
            content="Was active, now expired",
            active_from=now - timezone.timedelta(days=3),
            active_to=now - timezone.timedelta(days=1),
        )
        unending_news = NewsItem.objects.create(
            title="Always Active News",
            content="No end date",
            active_from=now - timezone.timedelta(days=5),
            active_to=None,
        )

        # Request home page
        response = self.client.get(reverse("home"))

        # Active items should be shown
        self.assertContains(response, active_news.title)
        self.assertContains(response, unending_news.title)

        # Inactive items should not be shown
        self.assertNotContains(response, future_news.title)
        self.assertNotContains(response, expired_news.title)

    def test_news_carousel_navigation_button_visibility(self):
        """
        Verify that carousel navigation buttons are hidden when there is only
        one active news item and shown when there are two or more active items.
        """
        now = timezone.now()

        # Carousel navigation buttons should not show with one item
        NewsItem.objects.create(
            title="First News Item",
            content="First active news item",
            active_from=now - timezone.timedelta(days=1),
            active_to=now + timezone.timedelta(days=1),
        )
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "carousel-control-prev")
        self.assertNotContains(response, "carousel-control-next")

        # Carousel navigation buttons should show with two items
        NewsItem.objects.create(
            title="Second News Item",
            content="Second active news item",
            active_from=now - timezone.timedelta(days=1),
            active_to=now + timezone.timedelta(days=1),
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "carousel-control-prev")
        self.assertContains(response, "carousel-control-next")
