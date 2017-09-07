from django.contrib import admin
from django.contrib.admin import register

from .models import FrontendDeployment


@register(FrontendDeployment)
class FrontendDeploymentModelAdmin(admin.ModelAdmin):
    pass
