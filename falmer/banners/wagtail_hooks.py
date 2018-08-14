from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Banner


class BannerAdmin(ModelAdmin):
    model = Banner
    menu_icon = 'banner'
    menu_order = 350
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('heading', 'purpose', 'outlet')
    search_fields = ('heading', )


class GlobalAdminGroup(ModelAdminGroup):
    menu_label = 'Global'
    menu_icon = 'folder-open-inverse'
    menu_order = 300
    items = (BannerAdmin, )


modeladmin_register(GlobalAdminGroup)
