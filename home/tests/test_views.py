from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_homepage_returns_correct_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_returns_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/home.html")

    def test_homepage_has_hidden_title(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<h1 class="visually-hidden"')
        self.assertContains(response, 'City and District Table Tennis League')

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
            response,
            'alt="City and District Table Tennis League Logo Overlay"'
        )

    # About Section
    def test_homepage_contains_about_section(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, '<section id="about"')
        self.assertContains(
            response, "Welcome to the City and District Table Tennis League!"
        )
        self.assertContains(response, "Founded in 2015")
