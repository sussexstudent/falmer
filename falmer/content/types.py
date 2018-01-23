import graphene
from graphene.types.generic import GenericScalar
from wagtail.wagtailcore.blocks import StreamValue

from falmer.content.serializers import WagtailImageSerializer
from falmer.content.utils import underscore_to_camel, change_dict_naming_convention
from falmer.matte.models import MatteImage


class Page(graphene.ObjectType):
    type = graphene.String()

    title = graphene.String()
    slug = graphene.String()
    last_published_at = graphene.String()

    url_path = graphene.String()
    path = graphene.String()

    data = GenericScalar()

    sub_pages = graphene.List(lambda: Page)
    parent_page = graphene.Field(lambda: Page)
    ancestors = graphene.List(lambda: Page)


    def resolve_type(self, info):
        return self.__class__.__name__

    def resolve_title(self, info):
        return self.title

    def resolve_slug(self, info):
        return self.slug

    def resolve_last_published_at(self, info):
        return self.last_published_at

    def resolve_url_path(self, info):
        return self.url_path

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
        return self.get_children().live()

    def resolve_ancestors(self, info):
        return self.get_ancestors()
