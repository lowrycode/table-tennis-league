from django.contrib import admin
from .models import Division, Season


# Register your models here.
@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name", "rank")


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "is_current")
    prepopulated_fields = {"slug": ("short_name",)}
