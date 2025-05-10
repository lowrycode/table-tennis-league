from django.test import TestCase
from django.urls import reverse


class ContactPageTests(TestCase):
    def test_contact_page_returns_correct_status_code(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_returns_correct_template(self):
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, "contact/contact.html")

    def test_contact_page_has_title(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Contact Us")

    def test_contact_page_has_contact_details_section(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response, '<section id="contact-details"')
        self.assertContains(response, "League and Website Administrator:")
        self.assertContains(response, 'href="mailto:')
        self.assertContains(response, 'href="tel:')
