from django.contrib import admin
from django.contrib.admin import register
from . import models

@register(models.FalmerUser)
class FalmerUserModelAdmin(admin.ModelAdmin):
    list_display = ('name_or_email', 'identifier', 'authority')
    list_filter = ('authority', )
    search_fields = ('name', 'identifier')

