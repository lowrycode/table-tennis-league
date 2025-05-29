from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangeEmailForm(forms.ModelForm):
    """
    A form for updating a user's email address.

    The email input is converted to lowercase and validated to ensure
    uniqueness across all users (excluding the current user).
    """
    class Meta:
        model = User
        fields = ["email"]
        labels = {
            "email": "New Email",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        """
        Validates the email field to ensure it is unique after converting
        to lowercase.

        Raises:
            forms.ValidationError: If email is already in use.

        Returns:
            str: The cleaned and validated email address.
        """
        # Force lowercase
        email = self.cleaned_data["email"].lower()

        # Check email is unique
        if (
            User.objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "This email is already in use by another account."
            )
        return email
