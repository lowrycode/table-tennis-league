from django.contrib import admin
from .models import Club, ClubInfo

# Register your models here.
admin.site.register(Club)


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ("club", "created_on", "approved")
    list_filter = ("approved",)
