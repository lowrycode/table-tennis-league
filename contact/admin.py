from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'submitted_at', 'is_actioned')
    list_filter = ('is_actioned',)
