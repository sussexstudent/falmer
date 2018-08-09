from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import Event, Venue, Category, BrandingPeriod, Type


class EventAdmin(ModelAdmin):
    model = Event
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'start_time', 'embargo_until')
    list_filter = ('embargo_until', )
    search_fields = ('title',)


class VenueAdmin(ModelAdmin):
    model = Venue
    menu_icon = 'site'  # change as required
    menu_order = 250  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', )
    search_fields = ('name',)


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_icon = 'site'  # change as required
    menu_order = 250  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', )
    search_fields = ('name',)


class TypeAdmin(ModelAdmin):
    model = Type
    menu_icon = 'site'  # change as required
    menu_order = 250  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', )
    search_fields = ('name',)


class BrandingPeriodAdmin(ModelAdmin):
    model = BrandingPeriod
    menu_icon = 'site'  # change as required
    menu_order = 250  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', )
    search_fields = ('name',)


class EventsGroupAdmin(ModelAdminGroup):
    menu_label = 'Events'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (EventAdmin, VenueAdmin, CategoryAdmin, TypeAdmin, BrandingPeriodAdmin)


modeladmin_register(EventsGroupAdmin)
