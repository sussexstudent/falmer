from django.contrib import admin
from django.contrib.admin import register

from .models import MatteImage, MatteRendition, RemoteImage


@register(MatteImage)
class MatteImageModelAdmin(admin.ModelAdmin):
    pass


@register(MatteRendition)
class MatteRenditionModelAdmin(admin.ModelAdmin):
    pass


@register(RemoteImage)
class RemoteImageModelAdmin(admin.ModelAdmin):
    pass
