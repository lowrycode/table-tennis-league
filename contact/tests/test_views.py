from django.test import TestCase
from django.urls import reverse
from contact.forms import EnquiryForm
from django.contrib.auth import get_user_model
from contact.models import Enquiry
from django.contrib import messages

User = get_user_model()


class ContactPageTests(TestCase):
    """
    Tests for the Contact page view, covering rendering, form behavior
    and valid/invalid submission handling.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a test user for authenticated user-related test cases.
        """
        cls.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )

    # Test page renders correctly for static elements
    def test_contact_page_returns_correct_status_code(self):
        """
        Verify Contact page returns status code 200.
        """
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_returns_correct_template(self):
        """
        Verify Contact page uses the expected template.
        """
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, "contact/contact.html")

    def test_contact_page_has_title(self):
        """
        Verify page title and heading elements are present.
        """
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Contact Us")

    def test_contact_page_has_contact_details_section(self):
        """
        Verify contact details section and its content are present.
        """
        response = self.client.get(reverse("contact"))
        self.assertContains(response, 'id="contact-details"')
        self.assertContains(response, "League and Website Administrator:")
        self.assertContains(response, 'href="mailto:')
        self.assertContains(response, 'href="tel:')

    def test_contact_page_has_enquiries_section(self):
        """
        Verify enquiries section and expected categories are present.
        """
        response = self.client.get(reverse("contact"))
        self.assertContains(response, '<section id="enquiries"')
        self.assertContains(response, "Club Enquiries")
        self.assertContains(response, "League Enquiries")
        self.assertContains(response, "Other Enquiries")

    # Test form rendering for GET request
    def test_contact_page_renders_form(self):
        """
        Verify enquiry form renders on GET request.
        """
        response = self.client.get(reverse("contact"))
        self.assertContains(response, 'id="enquiry-form"')
        self.assertContains(response, '<input type="text"')
        self.assertContains(response, "<label")
        self.assertContains(response, "Contact Number")  # A custom label
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], EnquiryForm)

    def test_page_contains_csrf(self):
        """
        Verify page includes CSRF token for form submission.
        """
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_enquiry_form_prefills_email_for_authenticated_user(self):
        """
        Verify form pre-fills the email field for authenticated users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].initial["email"], self.user.email
        )

    def test_enquiry_form_email_not_prefilled_for_unauthenticated_user(self):
        """
        Verify email is not pre-filled for anonymous users.
        """
        response = self.client.get(reverse("contact"))
        self.assertNotIn("email", response.context["form"].initial)

    # Test valid form submissions with POST request
    def test_authenticated_user_can_submit_valid_enquiry_form(self):
        """
        Verify authenticated users can submit a valid enquiry.
        """
        self.client.force_login(self.user)
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "01234567890",
            "subject": "Test Subject",
            "message": "Test message content.",
        }
        response = self.client.post(reverse("contact"), form_data, follow=True)
        self.assertRedirects(response, reverse("contact"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Your enquiry has been submitted successfully.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

        # Check database entry
        self.assertEqual(Enquiry.objects.count(), 1)
        enquiry = Enquiry.objects.get(subject="Test Subject")
        self.assertEqual(enquiry.user, self.user)
        self.assertEqual(enquiry.name, form_data["name"])
        self.assertEqual(enquiry.email, form_data["email"])
        self.assertEqual(enquiry.phone, form_data["phone"])
        self.assertEqual(enquiry.subject, form_data["subject"])
        self.assertEqual(enquiry.message, form_data["message"])

    def test_unauthenticated_user_can_submit_valid_enquiry_form(self):
        """
        Verify unauthenticated users can submit a valid enquiry.
        """
        form_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "01234567890",
            "subject": "Test Subject",
            "message": "Test message content.",
        }
        response = self.client.post(reverse("contact"), form_data, follow=True)
        self.assertRedirects(response, reverse("contact"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Your enquiry has been submitted successfully.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

        # Check database entry
        self.assertEqual(Enquiry.objects.count(), 1)
        enquiry = Enquiry.objects.get(subject="Test Subject")
        self.assertEqual(enquiry.user, None)
        self.assertEqual(enquiry.name, form_data["name"])
        self.assertEqual(enquiry.email, form_data["email"])
        self.assertEqual(enquiry.phone, form_data["phone"])
        self.assertEqual(enquiry.subject, form_data["subject"])
        self.assertEqual(enquiry.message, form_data["message"])

    # Test Invalid form submissions
    def test_invalid_form_submission_shows_warning(self):
        """
        Check that invalid form submissions return warnings and form errors.
        """
        form_data = {
            "name": "",  # Missing required field
            "email": "invalid_email_address",
            "phone": "",
            "subject": "",
            "message": "",
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "name", "This field is required."
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
