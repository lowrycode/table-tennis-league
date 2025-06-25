from django import template

register = template.Library()


@register.filter
def status_class(value):
    """
    Returns a CSS class name based on the fixture status.

    If the value matches one of the recognized statuses
    (scheduled, postponed, cancelled or completed) it returns
    'fixture-<status>'. Otherwise, it returns 'fixture-status-none'.

    Args:
        value (str): The status string to evaluate.

    Returns:
        str: Corresponding CSS class for the status.
    """
    status_set = {"scheduled", "postponed", "cancelled", "completed"}
    if value in status_set:
        return f"fixture-{value}"
    return "fixture-status-none"
