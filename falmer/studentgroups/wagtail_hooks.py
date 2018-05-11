from wagtail.contrib.modeladmin.options import (
        ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import StudentGroup, AwardAuthority, AwardPeriod, Award, GroupAwarded


class StudentGroupAdmin(ModelAdmin):
    model = StudentGroup
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('name', 'is_prospective')
    list_filter = ('is_prospective', )
    search_fields = ('name',)


class AwardAuthorityAdmin(ModelAdmin):
    model = AwardAuthority
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('name',)
    search_fields = ('name',)


class AwardAdmin(ModelAdmin):
    model = Award
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('name',)
    search_fields = ('name',)


class AwardPeriodAdmin(ModelAdmin):
    model = AwardPeriod
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('display_name', 'authority')
    search_fields = ('display_name',)


class GroupAwardedAdmin(ModelAdmin):
    model = GroupAwarded
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('group', 'award', 'period', 'grade')


class StudentGroupAdminGroup(ModelAdminGroup):
    menu_label = 'Student Groups'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (StudentGroupAdmin, GroupAwardedAdmin, AwardAdmin, AwardAuthorityAdmin)

modeladmin_register(StudentGroupAdminGroup)
