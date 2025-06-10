from django import template

register = template.Library()


@register.filter
def status_class(value):
    status_set = {"scheduled", "postponed", "cancelled", "completed"}
    if value in status_set:
        return f"fixture-{value}"
    return "fixture-status-none"
