from django.contrib import admin
from django.contrib.admin import register
from . import models

@register(models.FalmerUser)
class FalmerUserModelAdmin(admin.ModelAdmin):
    pass

