from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.Slate)
class SlateModelAdmin(admin.ModelAdmin):
    pass

