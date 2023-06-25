from django.contrib import admin
from .models import Event, Event_status

# Register your models here.
# admin.site.register(Event)

admin.site.register(Event_status)

def change_status_to_upcoming(queryset):
    queryset.update(event_status='upcoming')
    change_status_to_upcoming.short_description = "change selected events status to upcoming"


def change_status_to_current(queryset):
    queryset.update(event_status='current')
    change_status_to_current.short_description = "change selected events status to current"

def change_status_to_finished(queryset):
    queryset.update(event_status='finished')
    change_status_to_finished.short_description = "change selected events status to finished"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_id', 'support_contact', 'date_created', 'date_updated', 'attendees', 'event_status', 'event_date', 'contract']
    search_fields = ['client_id', 'support_contact', 'date_created', 'date_updated', 'event_status', 'event_date', 'contract']
    list_filter = ['date_created', 'date_updated', 'event_status', 'event_date']
    actions = [change_status_to_upcoming, change_status_to_current, change_status_to_finished]