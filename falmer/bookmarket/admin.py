from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.Listing)
class ListingModelAdmin(admin.ModelAdmin):
    pass


@register(models.ListingSection)
class ListingSectionModelAdmin(admin.ModelAdmin):
    pass

