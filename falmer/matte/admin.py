from django.contrib import admin
from django.contrib.admin import register

from .models import MatteImage, MatteRendition, RemoteImage, ImageLabel, ImageLabelThrough, ImageExternalMetadata


@register(MatteImage)
class MatteImageModelAdmin(admin.ModelAdmin):
    pass


@register(MatteRendition)
class MatteRenditionModelAdmin(admin.ModelAdmin):
    pass


@register(RemoteImage)
class RemoteImageModelAdmin(admin.ModelAdmin):
    pass


@register(ImageLabel)
class ImageLabelModelAdmin(admin.ModelAdmin):
    pass


@register(ImageLabelThrough)
class ImageLabelThroughModelAdmin(admin.ModelAdmin):
    pass


@register(ImageExternalMetadata)
class ImageExternalMetadataModelAdmin(admin.ModelAdmin):
    pass
