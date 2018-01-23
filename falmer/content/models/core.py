from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from wagtail.wagtailcore.models import Page as WagtailPage


class Page(WagtailPage):
    is_creatable = False

    def serve(self, request, *args, **kwargs):
        if not settings.MSL_SITE_HOST:
            return HttpResponse('MSL_SITE_HOST not set in settings')

        site_id, root_path, root_url = self.get_url_parts()

        return redirect(f'{settings.MSL_SITE_HOST}/content-explorer?path={root_url}')

    def get_live_children(self):
        return self.get_children().live()

    class Meta:
        proxy = True
