from django.urls import reverse
import django_filters
from .models import Fixture, Season, Division


class FixtureFilter(django_filters.FilterSet):
    season = django_filters.ModelChoiceFilter(
        queryset=Season.objects.filter(is_visible=True),
        to_field_name="slug",
        label="Season",
        empty_label=None,
    )
    division = django_filters.ModelChoiceFilter(
        queryset=Division.objects.none(),  # populated dynamically
        empty_label="All Divisions",
    )

    def __init__(self, data=None, *args, **kwargs):
        # Set current season as default
        if not data or not data.get("season"):
            current_season = Season.objects.filter(is_current=True).first()
            if current_season:
                data = data.copy() if data else {}
                data["season"] = current_season.slug
        super().__init__(data, *args, **kwargs)

        # Update filter dropdowns if trigger field is changed
        trigger_fields = {"season", }

        for field_name in trigger_fields:
            field = self.form.fields.get(field_name)
            if field:
                field.widget.attrs.update(
                    {
                        "hx-get": reverse("fixtures_filter"),
                        "hx-target": "#filter-fixtures",
                        "hx-trigger": "change",
                        "hx-swap": "innerHTML",
                        "hx-include": "closest form",  # to send all fields
                    }
                )

        # Adjust division queryset based on selected season
        season_slug = self.data.get("season")
        if season_slug:
            try:
                season = Season.objects.get(slug=season_slug)
                self.form.fields["division"].queryset = season.divisions.all()
            except Season.DoesNotExist:
                self.form.fields["division"].queryset = Division.objects.none()

    class Meta:
        model = Fixture
        fields = ["season", "division"]
