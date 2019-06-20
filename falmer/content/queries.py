import graphene
from django.http import Http404
from wagtail.core.models import Page
from falmer.content.models import PreviewData
from . import types


class Query(graphene.ObjectType):
    page = graphene.Field(types.Page, path=graphene.String(), preview_token=graphene.String())
    all_pages = graphene.List(types.Page, path=graphene.String())

    def resolve_page(self, info, **kwargs):
        path = kwargs.get('path')
        path = path[1:] if path.startswith('/') else path
        path = path[:-1] if path.endswith('/') else path

        root_page = info.context.site.root_page

        # if we're given a preview token, return the model it's acc. with
        # instead of routing it within live pages
        preview_token = kwargs.get('preview_token')
        if preview_token:
            preview = PreviewData.objects.get(token=preview_token)

            return preview.get_preview_model()

        if path == '':
            return root_page

        path_components = path.split('/')

        for lim in range(len(path_components), 0, -1):
            try:
                result = root_page.route(info.context, path_components[:lim])

                return result.page
            except Http404:
                continue

        return None

    def resolve_all_pages(self, info):
        return Page.objects.specific().live()
