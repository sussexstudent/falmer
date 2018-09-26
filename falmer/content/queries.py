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

        if path == '':
            return root_page

        path_components = path.split('/')

        for lim in range(len(path_components), 1, -1):
            try:
                print('trying', path_components[:lim])
                result = root_page.route(info.context, path_components[:lim])
                return result.page
            except Http404:
                continue

        return None

    def resolve_all_pages(self, info):
        return Page.objects.specific().live()
