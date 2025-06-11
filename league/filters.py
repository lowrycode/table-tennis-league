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
        queryset=Division.objects.all(),
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

    class Meta:
        model = Fixture
        fields = ["season", "division"]
