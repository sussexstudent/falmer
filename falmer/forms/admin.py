from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.ConsentCodeForm)
class ConsentCodeFormModelAdmin(admin.ModelAdmin):
    pass


@register(models.ConsentCodeAuthorisation)
class ConsentCodeAuthorisationModelAdmin(admin.ModelAdmin):
    pass

