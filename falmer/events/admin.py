from django.contrib import admin
from django.contrib.admin import register

from falmer.events.models import Event, MSLEvent, Venue, AutoLocationDisplayToVenue


@register(Venue)
class VenueModelAdmin(admin.ModelAdmin):
    pass

@register(AutoLocationDisplayToVenue)
class VenueModelAdmin(admin.ModelAdmin):
    list_display = ('location', 'venue')

@register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', )

@register(MSLEvent)
class MSLEventModelAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'last_sync', 'disable_sync', )

    def get_title(self, obj):
        return obj.event.title
    get_title.admin_order_field = 'title'  #Allows column order sorting
    get_title.short_description = 'Event Title'  #Renames column head
