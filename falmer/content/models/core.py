from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
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
