from django.contrib import admin
from .models import EventListing

# Register your models here.
@admin.register(EventListing)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['eventID', 'image', 'title', 'description', 'posted', 'deadline', 'now']
