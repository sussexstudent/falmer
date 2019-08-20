from django.contrib import admin
from django.contrib.admin import register
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from falmer.events.models import Event, MSLEvent, Venue, AutoLocationDisplayToVenue, \
    BrandingPeriod, Type, Bundle, CategoryNode, EventLike


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


@register(EventLike)
class EventLikeModelAdmin(admin.ModelAdmin):
    list_display = ('get_event_title', 'get_user_id', 'source')

    def get_event_title(self, obj):
        return obj.event.title

    def get_user_id(self, obj):
        return obj.user.id


@register(BrandingPeriod)
class BrandingPeriodModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@register(CategoryNode)
class CategoryModelAdmin(TreeAdmin):
    list_display = ('name', )
    form = movenodeform_factory(CategoryNode)


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
