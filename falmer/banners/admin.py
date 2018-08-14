from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.Banner)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ('heading', 'outlet', 'purpose', 'is_active')
