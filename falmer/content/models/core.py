from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.models import Page as WagtailPage

from falmer.content.utils import get_public_path_for_page


class Page(WagtailPage):
    is_creatable = False

    def serve(self, request, *args, **kwargs):
        if not settings.MSL_SITE_HOST:
            return HttpResponse('MSL_SITE_HOST not set in settings')

        return redirect(f'{settings.MSL_SITE_HOST}{self.public_path}')

    def get_live_children(self):
        return self.get_children().live()

    class Meta:
        proxy = True

    def get_assumption_path(self):
        return None

    @property
    def public_path(self):
        return get_public_path_for_page(self)


class ClickThrough(Page):
    target_page = models.ForeignKey('content.Page', models.SET_NULL, 'click_throughs', blank=True, null=True)
    target_link = models.TextField(blank=True, default='')

    @property
    def public_path(self):
        if self.target_page:
            return self.target_page.public_path

        return self.target_link

    content_panels = Page.content_panels + [
        PageChooserPanel('target_page'),
        FieldPanel('target_link'),
    ]
