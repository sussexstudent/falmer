from django.contrib import admin
from django.contrib.admin import register

from falmer.events.models import Event


@register(Event)
class EventModelAdmin(admin.ModelAdmin):
    pass
