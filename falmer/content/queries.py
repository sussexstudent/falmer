import graphene
from django.http import Http404
from wagtail.core.models import Page

from . import types


class Query(graphene.ObjectType):
    page = graphene.Field(types.Page, path=graphene.String())
    all_pages = graphene.List(types.Page, path=graphene.String())

    def resolve_page(self, info, **kwargs):
        path = kwargs.get('path')
        path = path[1:] if path.startswith('/') else path
        path = path[:-1] if path.endswith('/') else path

        root_page = info.context.site.root_page

        try:
            if path == '':
                return root_page

            result = root_page.route(info.context, path.split('/'))
            return result.page
        except Http404:
            return None

    def resolve_all_pages(self, info):
        return Page.objects.specific().live()
