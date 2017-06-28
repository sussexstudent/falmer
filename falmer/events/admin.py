from django.contrib import admin
from django.contrib.admin import register

from falmer.events.models import Event, MSLEvent


@register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', )

@register(MSLEvent)
class MSLEventModelAdmin(admin.ModelAdmin):
    pass
