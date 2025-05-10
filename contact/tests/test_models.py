from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase
from contact.models import Enquiry


class EnquiryTests(TestCase):
    def setUp(self):
        self.enquiry = Enquiry(
            name="John",
            email="example@example.com",
            subject="My Sample Title",
            message="Just a test",
        )

    def test_can_create_enquiry(self):
        self.enquiry.full_clean()
        self.enquiry.save()
        self.assertEqual(self.enquiry.name, "John")
        self.assertEqual(self.enquiry.subject, "My Sample Title")
        self.assertEqual(self.enquiry.message, "Just a test")
        self.assertTrue(Enquiry.objects.filter(id=self.enquiry.id).exists())

    def test_string_representation(self):
        self.assertEqual(str(self.enquiry), "My Sample Title")

    def test_submitted_at_defaults_to_now(self):
        self.enquiry.save()
        now = timezone.now()
        self.assertTrue(
            now - timezone.timedelta(seconds=5)
            <= self.enquiry.submitted_at
            <= now + timezone.timedelta(seconds=5)
        )

    def test_is_actioned_defaults_to_false(self):
        self.enquiry.save()
        self.assertFalse(self.enquiry.is_actioned)

    def test_mark_as_actioned(self):
        self.enquiry.save()
        self.enquiry.is_actioned = True
        self.enquiry.save()
        self.assertTrue(Enquiry.objects.get(id=self.enquiry.id).is_actioned)

    def test_email_is_required_field(self):
        self.enquiry.email = None
        with self.assertRaises(ValidationError):
            self.enquiry.full_clean()
