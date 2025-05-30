from django.contrib import admin
from .models import NewsItem


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "active_from", "active_to")
    list_filter = ("active_from", "active_to")
