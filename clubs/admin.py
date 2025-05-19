from django.contrib import admin
from .models import Club, ClubInfo, Venue, VenueInfo, ClubVenue, ClubAdmin

# Register your models here.
admin.site.register(Club)
admin.site.register(Venue)
admin.site.register(ClubVenue)


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ("club", "created_on", "approved")
    list_filter = ("approved",)


@admin.register(VenueInfo)
class VenueInfoAdmin(admin.ModelAdmin):
    list_display = ("venue", "created_on", "approved")
    list_filter = ("approved",)


@admin.register(ClubAdmin)
class ClubAdminAdmin(admin.ModelAdmin):
    list_display = ("user", "club")
    list_filter = ("club",)
