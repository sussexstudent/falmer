import graphene
from graphene.types.generic import GenericScalar
from wagtail.wagtailcore.blocks import StreamValue

from falmer.content.serializers import WagtailImageSerializer
from falmer.matte.models import MatteImage


class Page(graphene.ObjectType):
    title = graphene.String()
    type = graphene.String()
    slug = graphene.String()
    url_path = graphene.String()
    data = GenericScalar()
    sub_pages = graphene.List(lambda: Page)
    parent_page = graphene.Field(lambda: Page)

    def resolve_title(self, info):
        return self.title

    def resolve_type(self, info):
        return self.__class__.__name__

    def resolve_slug(self, info):
        return self.slug

    def resolve_url_path(self, info):
        return self.url_path

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
        return data

    def resolve_parent_page(self, info):
        return self.get_parent()

    def resolve_sub_pages(self, info):
        return self.get_children().live()
