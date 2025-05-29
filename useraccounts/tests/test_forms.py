from django.test import TestCase
from useraccounts.forms import ChangeEmailForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangeEmailFormTests(TestCase):
    """
    Unit tests for the ChangeEmailForm to verify field behavior, validation,
    and functionality related to email updates.
    """
    def test_form_field_label(self):
        """Verify 'email' field has correct label."""
        form = ChangeEmailForm()
        self.assertEqual(form.fields["email"].label, "New Email")

    def test_blank_field(self):
        """Verify form is invalid when the email field is left blank."""
        data = {"email": ""}
        form = ChangeEmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_email_format(self):
        """
        Verify form is invalid when an improperly formatted email is submitted.
        """
        data = {"email": "invalid_email_address"}
        form = ChangeEmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_duplicate_email_not_allowed(self):
        """
        Verify that the form rejects an email address that already exists
        for another user.
        """
        user = User.objects.create_user(
            username="currentuser",
            email="something@example.com",
            password="Notrelevantforthistest!",
        )

        # Create another user with existing email
        User.objects.create_user(
            username="other",
            email="exists@example.com",
            password="Ialreadyhaveyouremail!",
        )

        # Check can't submit form if email already exists
        data = {"email": "exists@example.com"}
        form = ChangeEmailForm(data=data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_email_is_lowercased_on_save(self):
        """
        Verify that the email is converted to lowercase when the form is saved.
        """
        user = User.objects.create_user(
            username="lowercaseuser",
            email="initial@example.com",
            password="whateverisfine!",
        )

        data = {"email": "NEW.Email@Example.COM"}
        form = ChangeEmailForm(data=data, instance=user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, "new.email@example.com")

    def test_valid_form(self):
        """
        Verify that a form with a properly formatted and unique email is valid.
        """
        data = {"email": "mynewemail@example.com"}
        form = ChangeEmailForm(data=data)
        self.assertTrue(form.is_valid())
