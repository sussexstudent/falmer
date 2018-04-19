from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.Flag)
class FlagModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'mode')
    list_filter = ('state', 'mode', 'expired')

