from django.contrib import admin
from django.contrib.admin import register

from falmer.events.models import Event, MSLEvent, Venue, AutoLocationDisplayToVenue, BrandingPeriod, Category, Type, Bundle


@register(Venue)
class VenueModelAdmin(admin.ModelAdmin):
    pass

@register(AutoLocationDisplayToVenue)
class VenueModelAdmin(admin.ModelAdmin):
    list_display = ('location', 'venue')


@register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', )


@register(Bundle)
class BundleModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(BrandingPeriod)
class BrandingPeriodModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(Type)
class TypeModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(MSLEvent)
class MSLEventModelAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'last_sync', 'disable_sync', )

    def get_title(self, obj):
        return obj.event.title
    get_title.admin_order_field = 'title'  #Allows column order sorting
    get_title.short_description = 'Event Title'  #Renames column head
