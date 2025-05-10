from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from contact.models import Enquiry

User = get_user_model()


class EnquiryTests(TestCase):
    def setUp(self):
        self.enquiry = Enquiry.objects.create(
            name="John",
            email="example@example.com",
            phone="01233 455677",
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

    def test_phone_is_optional_field(self):
        self.enquiry.phone = None
        self.enquiry.full_clean()  # Should pass because phone is optional
        self.enquiry.save()
        self.assertIsNone(self.enquiry.phone)

    def test_invalid_phone_number(self):
        # Test not a number
        self.enquiry.phone = "Invalid"
        with self.assertRaises(ValidationError):
            self.enquiry.full_clean()

        # Test invalid region
        self.enquiry.phone = "4155552671"  # US phone number
        with self.assertRaises(ValidationError):
            self.enquiry.full_clean()

    def test_enquiry_user_relationship(self):
        user = User.objects.create_user(
            username="testuser",
            email="example@example.com",
            password="password123"
            )
        self.enquiry.user = user
        self.enquiry.full_clean()
        self.enquiry.save()

        self.assertEqual(self.enquiry.user, user)
        self.assertIn(self.enquiry, user.enquiries.all())

    def test_enquiries_are_ordered_desc_by_submitted_at(self):
        # Create older enquiry
        older = Enquiry.objects.create(
            name="Older",
            email="older@example.com",
            phone="01233 455677",
            subject="Older Enquiry",
            message="Older message"
        )
        # Override submitted_at
        older.submitted_at = timezone.now() - timezone.timedelta(days=1)
        older.save()

        # Create newer enquiry
        newer = Enquiry.objects.create(
            name="newer",
            email="newer@example.com",
            phone="01233 455677",
            subject="Newer Enquiry",
            message="Newer message"
        )
        # Override submitted_at
        newer.submitted_at = timezone.now() + timezone.timedelta(days=1)
        newer.save()

        enquiries = list(Enquiry.objects.all())
        self.assertEqual(enquiries[0], newer)
        self.assertEqual(enquiries[1], self.enquiry)
        self.assertEqual(enquiries[2], older)
