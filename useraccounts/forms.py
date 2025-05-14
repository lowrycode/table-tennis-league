from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangeEmailForm(forms.ModelForm):
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
