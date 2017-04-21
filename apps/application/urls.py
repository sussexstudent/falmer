"""services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from graphene_django.views import GraphQLView
from wagtail.wagtailimages.views.serve import ServeView

from apps.auth import urls as auth_urls
from apps.slack import urls as slack_urls
from apps.launcher import urls as launcher_urls

urlpatterns = [
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(action='redirect'), name='wagtailimages_serve'),
    url(r'^admin/', admin.site.urls),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    url(r'^auth/', include(auth_urls)),
    url(r'^slack/', include(slack_urls)),

    url(r'^$', include(launcher_urls)),
]
