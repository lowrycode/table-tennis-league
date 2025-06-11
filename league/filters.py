from django.urls import reverse
import django_filters
from .models import Fixture, Season, Division
from clubs.models import Club


class FixtureFilter(django_filters.FilterSet):
    """
    A dynamic filter for the Fixture model based on season, division, and club.

    - Season is required and defaults to the current season.
    - Division options are populated based on the selected season.
    - Club options are populated based on the selected season and division.
    - HTMX used to dynamically update filter options without full page reload.
    """

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
    club = django_filters.ModelChoiceFilter(
        queryset=Club.objects.none(),  # populated dynamically
        method="filter_by_club",
        label="Club (Home or Away)",
        empty_label="All Clubs",
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
        trigger_fields = {"season", "division"}

        for field_name in trigger_fields:
            field = self.form.fields.get(field_name)
            if field:
                field.widget.attrs.update(
                    {
                        "data-hx-get": reverse("fixtures_filter"),
                        "data-hx-target": "#filter-fixtures",
                        "data-hx-trigger": "change",
                        "data-hx-swap": "innerHTML",
                        "data-hx-include": "closest form",  # send all field
                    }
                )

        # Adjust division queryset based on season
        season = None
        season_slug = self.data.get("season")

        if season_slug:
            try:
                season = Season.objects.get(slug=season_slug)
                self.form.fields["division"].queryset = season.divisions.all()
            except Season.DoesNotExist:
                self.form.fields["division"].queryset = Division.objects.none()

        # Adjust club queryset based on division and/or season
        division_id = self.data.get("division")
        if season and division_id:
            try:
                division = Division.objects.get(id=division_id)
                self.form.fields["club"].queryset = Club.objects.filter(
                    club_teams__season=season, club_teams__division=division
                ).distinct()
            except Division.DoesNotExist:
                self.form.fields["club"].queryset = Club.objects.none()
        elif season:
            # No division selected: show all clubs in the season
            self.form.fields["club"].queryset = Club.objects.filter(
                club_teams__season=season
            ).distinct()

    class Meta:
        model = Fixture
        fields = ["season", "division", "club"]

    def filter_by_club(self, queryset, name, value):
        """
        Filters the queryset to include fixtures where the selected club is
        either the home or away team.
        """
        return queryset.filter(home_team__club=value) | queryset.filter(
            away_team__club=value
        )
