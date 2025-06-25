from django.core.exceptions import ValidationError
from datetime import time


def validate_match_time(value):
    """
    Validates that the match time is between 6:00 PM and 8:00 PM (inclusive).

    Raises:
        ValidationError: If the time is outside the allowed range.
    """
    if not time(18, 0) <= value <= time(20, 0):
        raise ValidationError("Match must start between 6:00 PM and 8:00 PM.")
