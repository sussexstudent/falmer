from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import redirect_to_login
from django.urls import path, re_path, reverse
from django.views import defaults as default_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.images.views.serve import ServeView

# from config import saml_urls
from falmer.content.pages import PreviewOnEditRemix, view_draft
from falmer.schema.api import api_router
from falmer.auth import urls as auth_urls
from falmer.slack import urls as slack_urls
from falmer.matte import urls as matte_urls
from falmer.search import urls as search_urls
from falmer.schema import urls as schema_urls
from falmer.newsletters import urls as newsletters_urls
from falmer.frontend import urls as frontend_urls
from falmer.links import urls as links_urls


def redirect_to_my_auth(request):
    return redirect_to_login(reverse('wagtailadmin_home'), login_url='frontend')

urlpatterns = [
                  url(r'^cms/login', redirect_to_my_auth, name='wagtailadmin_login'),
                  url(settings.ADMIN_URL, admin.site.urls),

                  url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
                      ServeView.as_view(action=settings.IMAGE_SERVE_METHOD),
                      name='wagtailimages_serve'),
                  path('content-api/v2/', api_router.urls),
                  path('admin/', admin.site.urls),

                  re_path(r'^cms/pages/(\d+)/view_draft/$', view_draft, name='view_draft'),
                  re_path(r'^cms/pages/(\d+)/edit/preview/$', PreviewOnEditRemix.as_view(), name='preview_on_edit'),
                  re_path(r'^cms/', include(wagtailadmin_urls)),
                  path('documents/', include(wagtaildocs_urls)),
                  path('graphql/', include(schema_urls)),
                  path('auth/', include(auth_urls)),
                  path('slack/', include(slack_urls)),
                  path('images/', include(matte_urls)),
                  path('search/', include(search_urls)),
                  path('newsletters/', include(newsletters_urls)),
                  path('o/', include(links_urls)),
                  path('wagtail/', include(wagtail_urls)),

                  path('', include(frontend_urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
