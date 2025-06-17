from django import forms
from django.core.exceptions import ValidationError
from .models import DoublesMatch


class DoublesMatchAdminForm(forms.ModelForm):
    class Meta:
        model = DoublesMatch
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        fixture_result = cleaned_data.get("fixture_result")
        home_players = cleaned_data.get("home_players")
        away_players = cleaned_data.get("away_players")

        # Check each team has 2 players
        if home_players and home_players.count() != 2:
            raise ValidationError(
                {"home_players": "Exactly 2 home players must be selected."}
            )
        if away_players and away_players.count() != 2:
            raise ValidationError(
                {"away_players": "Exactly 2 away players must be selected."}
            )

        # Check for same player on both teams
        if home_players and away_players:
            if home_players.filter(id__in=away_players).exists():
                raise ValidationError("A player cannot be on both teams.")

        if fixture_result:
            fixture = fixture_result.fixture
            fixture_season = fixture.season

            # Validate home players
            if home_players:
                for hp in home_players:
                    if hp.team.season != fixture_season:
                        raise ValidationError(
                            "Home players must be from the same season as "
                            "the fixture."
                        )
                    if hp.team.club != fixture.home_team.club:
                        raise ValidationError(
                            f"{hp.player.full_name} does not belong to the "
                            "home team's club."
                        )

            # Validate away players
            if away_players:
                for ap in away_players:
                    if ap.team.season != fixture_season:
                        raise ValidationError(
                            "Away players must be from the same season as "
                            "the fixture."
                        )
                    if ap.team.club != fixture.away_team.club:
                        raise ValidationError(
                            f"{ap.player.full_name} does not belong to the "
                            "away team's club."
                        )

        return cleaned_data
