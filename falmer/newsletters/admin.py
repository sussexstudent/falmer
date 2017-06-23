from django.contrib import admin
from django.contrib.admin import register

from .models import MailChimpList


@register(MailChimpList)
class MailChimpListModelAdmin(admin.ModelAdmin):
    list_display = ('slug', 'enabled', 'mailchimp_list_id')
