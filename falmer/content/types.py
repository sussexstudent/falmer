import graphene
from graphene.types.generic import GenericScalar
from wagtail.core.blocks import StreamValue

from falmer.content import models
from falmer.content.serializers import WagtailImageSerializer
from falmer.content.utils import underscore_to_camel, change_dict_naming_convention
from falmer.matte.models import MatteImage


class Page(graphene.Interface):
    content_type = graphene.String()

    title = graphene.String()
    slug = graphene.String()

    seo_title = graphene.String()
    search_description = graphene.String()

    last_published_at = graphene.String()

    url_path = graphene.String()
    path = graphene.String()
    assumption_path = graphene.String()

    data = GenericScalar()

    sub_pages = graphene.List(lambda: Page)
    parent_page = graphene.Field(lambda: Page)
    ancestors = graphene.List(lambda: Page)

    def resolve_content_type(self, info):
        return self.__class__.__name__

    def resolve_title(self, info):
        return self.title

    def resolve_slug(self, info):
        return self.slug

    def resolve_seo_title(self, info):
        return self.seo_title

    def resolve_search_description(self, info):
        return self.search_description

    def resolve_last_published_at(self, info):
        return self.last_published_at

    def resolve_url_path(self, info):
        return self.url_path

    def resolve_assumption_path(self, info):
        return self.get_assumption_path()

    def resolve_path(self, info):
        if self.get_url_parts() is None:
            return None
        return self.get_url_parts()[2][6:]

    def resolve_data(self, info):
        data = dict()
        if hasattr(self.__class__, 'api_fields'):
            for field in self.__class__.api_fields:
                field_data = getattr(self, field)
                field_type = field_data.__class__
                if field_type is StreamValue:
                    data[field] = field_data.stream_block.get_api_representation(field_data, info.context)
                elif field_type in (str, bool, int, float):
                    data[field] = field_data
                elif field_type is MatteImage:
                    data[field] = WagtailImageSerializer(instance=field_data).data
                else:
                    data[field] = f'Unknown data type: {field_type.__name__}'
        return change_dict_naming_convention(data, underscore_to_camel)

    def resolve_parent_page(self, info):
        return self.get_parent()

    def resolve_sub_pages(self, info):
        return self.get_children().specific().live()

    def resolve_ancestors(self, info):
        return self.get_ancestors()

    @classmethod
    def resolve_type(cls, instance, info):
        name = instance.__class__.__name__
        if name in page_types_map:
            return page_types_map[name]

        return GenericPage


def generate_interfaces_for_type(page_models):
    types = {}
    meta = type('Meta', (), {
        'interfaces': (Page, )
    })

    for page in page_models:
        types[page.__name__] = type(page.__name__, (graphene.ObjectType, ), {
            'Meta': meta
        })

    return types

#
# class DetailedGuideSectionPage(graphene.ObjectType):
#     class Meta:
#         interfaces = (Page, )
#
page_types_map = generate_interfaces_for_type((
    models.StaffPage,
    models.SectionContentPage,
    models.SelectionGridPage,
    models.OfficerOverviewPage,
    models.HomePage,
    models.FreshersHomepage,
    models.ContentRootPage,
    models.AnswerPage,
    models.ReferencePage,
    models.DetailedGuidePage,
    models.DetailedGuideSectionPage,
))


class GenericPage(graphene.ObjectType):
    class Meta:
        interfaces = (Page, )
