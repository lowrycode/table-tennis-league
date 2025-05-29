from django.test import TestCase
from contact.forms import EnquiryForm


class EnquiryFormTests(TestCase):
    """
    Unit tests for the EnquiryForm to verify field labels, validation logic,
    and handling of valid and invalid input data.
    """
    def test_form_field_labels(self):
        """
        Verify that each form field has the correct label.
        """
        form = EnquiryForm()
        self.assertEqual(form.fields["name"].label, "Name")
        self.assertEqual(form.fields["email"].label, "Email")
        self.assertEqual(form.fields["phone"].label, "Contact Number")
        self.assertEqual(form.fields["subject"].label, "Subject")
        self.assertEqual(form.fields["message"].label, "Message")

    def test_valid_form(self):
        """
        Verify form is valid when all required fields are provided correctly.
        """
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '',
            'subject': 'Test Subject',
            'message': 'My test message.'
        }
        form = EnquiryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_with_missing_fields(self):
        """
        Verify form is invalid when required fields are missing.
        """
        data = {
            'name': '',
            'email': '',
            'phone': '',
            'subject': '',
            'message': ''
        }
        form = EnquiryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)

    def test_invalid_form_with_bad_email_format(self):
        """
        Verify form is invalid when email format is incorrect.
        """
        data = {
            'name': 'John Doe',
            'email': 'invalid_email_address',
            'phone': '',
            'subject': 'Test Subject',
            'message': 'My test message.'
        }
        form = EnquiryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
