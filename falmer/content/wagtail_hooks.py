from django.conf import settings
from django.http import HttpResponseRedirect
from wagtail.wagtailcore import hooks


@hooks.register('before_serve_page')
def redirect_to_website(page, request, serve_args, serve_kwargs):
    return HttpResponseRedirect(f'{settings.MSL_SITE_HOST}/content-explorer?path={request.path[6:]}')
