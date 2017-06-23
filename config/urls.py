from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.views.decorators.csrf import csrf_exempt
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from graphene_django.views import GraphQLView
from wagtail.wagtailimages.views.serve import ServeView

from falmer.schema.api import api_router
from falmer.auth import urls as auth_urls
from falmer.slack import urls as slack_urls
from falmer.launcher import urls as launcher_urls
from falmer.events import urls as events_urls
from falmer.search import urls as search_urls
from falmer.newsletters import urls as newsletters_urls

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(action=settings.IMAGE_SERVE_METHOD), name='wagtailimages_serve'),
    url(r'^content-api/v2/', api_router.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    url(r'^auth/', include(auth_urls)),
    url(r'^slack/', include(slack_urls)),
    url(r'^events/', include(events_urls)),
    url(r'^search/', include(search_urls)),
    url(r'^newsletters/', include(newsletters_urls)),

    url(r'^', include(launcher_urls)),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
