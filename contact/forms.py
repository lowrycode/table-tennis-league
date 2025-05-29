from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    """
    Form for submitting an enquiry on the Contacts page.
    """
    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "subject", "message"]
        labels = {
            "phone": "Contact Number",
        }
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "(optional)"}),
        }
