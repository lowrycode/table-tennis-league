from django.contrib import admin, messages
from .models import Division, Season


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name", "rank")

    def has_delete_permission(self, request, obj=None):
        """
        Disable delete permission from detail view if the division is
        linked to any season.
        """
        if obj and obj.seasons.exists():
            return False
        return super().has_delete_permission(request, obj)

    def get_actions(self, request):
        """
        Defines a custom delete function to run instead of the standard
        bulk delete function.
        """
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            actions["delete_selected"] = (
                self.delete_unlinked_divisions_only,
                "delete_selected",
                "Delete unlinked divisions",
            )
        return actions

    @staticmethod
    def delete_unlinked_divisions_only(modeladmin, request, queryset):
        """
        Deletes unlinked divisions but not divisions linked to a season.

        If divisions were deleted, a success message states how many.
        If linked divisions found, a warning message states those records were
        not deleted.
        """

        linked_ids = queryset.filter(seasons__isnull=False).values_list(
            "id", flat=True
        )
        unlinked = queryset.exclude(id__in=linked_ids)

        if unlinked.exists():
            count = unlinked.count()
            unlinked.delete()
            modeladmin.message_user(
                request,
                f"Successfully deleted {count} unlinked division(s).",
                level=messages.SUCCESS,
            )

        if linked_ids:
            names = queryset.filter(id__in=linked_ids).values_list(
                "name", flat=True
            )
            modeladmin.message_user(
                request,
                (
                    "Could not delete divisions linked to a season: "
                    f"{', '.join(names)}."
                ),
                level=messages.WARNING,
            )


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "is_current")
    prepopulated_fields = {"slug": ("short_name",)}
