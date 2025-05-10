from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from home.models import NewsItem


class HomePageStaticTests(TestCase):
    def test_homepage_returns_correct_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_returns_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/home.html")

    def test_homepage_has_hidden_title(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<h1 class="visually-hidden"')
        self.assertContains(response, "City and District Table Tennis League")

    # Hero Section
    def test_homepage_contains_hero_section(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="hero"')

    def test_homepage_contains_hero_image(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<picture>")
        self.assertContains(response, 'srcset="/static/images/hero.webp"')
        self.assertContains(response, 'srcset="/static/images/hero.jpg"')
        self.assertContains(response, "<img")
        self.assertContains(
            response, 'alt="Action shot of table tennis player in an arena"'
        )

    def test_homepage_contains_hero_overlay(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'id="hero-overlay"')
        self.assertContains(response, 'src="/static/images/hero-overlay.png"')
        self.assertContains(
            response, 'alt="City and District Table Tennis League Logo Overlay"'
        )

    # About Section
    def test_homepage_contains_about_section(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="about"')
        self.assertContains(
            response, "Welcome to the City and District Table Tennis League!"
        )
        self.assertContains(response, "Founded in 2015")

    # News Section
    def test_homepage_contains_news_section(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="news"')
        self.assertContains(response, "Latest News")

    # FAQ Section
    def test_homepage_contains_faq_section(self):
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
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="sponsors"')
        self.assertContains(response, "League Sponsors")
        self.assertContains(response, 'class="sponsor-img"')
        self.assertContains(response, 'rel="noopener noreferrer"')

    # Footer Section
    def test_homepage_contains_footer(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<footer")
        self.assertContains(response, '<section id="contact"')
        self.assertContains(response, 'class="social-media"')
        self.assertContains(response, "fa-brands fa-instagram")
        self.assertContains(response, "fa-brands fa-square-facebook")
        self.assertContains(response, "fa-brands fa-x-twitter")
        self.assertContains(response, "© 2025 Peter Lowry")


class HomePageDynamicNewsTests(TestCase):
    def test_homepage_displays_placeholder_when_no_news_items(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No news items to show at the moment.")
        self.assertNotContains(response, 'id="news-carousel"')

    def test_homepage_displays_only_active_news_items(self):
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
