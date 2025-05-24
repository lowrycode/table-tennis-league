from django import forms
from django_filters import FilterSet, BooleanFilter, ChoiceFilter
from .models import ClubInfo

MEMBERSHIP_BOOLEAN_CHOICES = (
    (True, "Required"),
    (False, "Not Required"),
)


class BooleanFilterCheckedOnly(BooleanFilter):
    def filter(self, qs, value):
        if value is True:
            return super().filter(qs, value)
        # If unchecked or None, don't filter
        return qs


class ClubInfoFilter(FilterSet):
    # Tick boxes
    beginners = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    intermediates = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    advanced = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    kids = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    adults = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    coaching = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    league = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    equipment_provided = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)
    free_taster = BooleanFilterCheckedOnly(widget=forms.CheckboxInput)

    # Select box
    membership_required = ChoiceFilter(
        choices=MEMBERSHIP_BOOLEAN_CHOICES,
        widget=forms.Select,
        label="Membership",
    )

    class Meta:
        model = ClubInfo
        fields = [
            "beginners",
            "intermediates",
            "advanced",
            "kids",
            "adults",
            "coaching",
            "league",
            "equipment_provided",
            "free_taster",
            "membership_required",
        ]
