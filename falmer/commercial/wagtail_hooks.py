from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Offer, OfferCategory


class OfferCategoryAdmin(ModelAdmin):
    model = OfferCategory
    menu_icon = 'site'
    menu_order = 250
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', )
    search_fields = ('name', )


class OfferAdmin(ModelAdmin):
    model = Offer
    menu_icon = 'site'
    menu_order = 250
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('deal_tag', 'company_name')
    search_fields = ('deal_tag', 'company_name')


class CommercialAdminGroup(ModelAdminGroup):
    menu_label = 'Commercial'
    menu_icon = 'folder-open-inverse'
    menu_order = 260
    items = (OfferAdmin, OfferCategoryAdmin, )


modeladmin_register(CommercialAdminGroup)
