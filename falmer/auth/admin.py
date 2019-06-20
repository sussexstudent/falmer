from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# @register(models.FalmerUser)
# class FalmerUserModelAdmin(admin.ModelAdmin):
#     list_display = ('name_or_email', 'identifier', 'authority')
#     list_filter = ('authority', )
#     search_fields = ('name', 'identifier')
from falmer.auth import models


class FalmerUserAdmin(UserAdmin):
    ordering = ('name', 'identifier')
    list_display = ('name_or_email', 'identifier', 'authority')

    fieldsets = (
        (None, {'fields': ('identifier', 'authority')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                                     })
    )


admin.site.register(models.FalmerUser, FalmerUserAdmin)
