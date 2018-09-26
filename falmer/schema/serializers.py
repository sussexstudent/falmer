from wagtail.api.v2.serializers import PageParentField as WagtailPageParentField
from wagtail.api.v2.serializers import PageSerializer as WagtailPageSerializer
from wagtail.api.v2.serializers import Field, StreamField, get_serializer_class


def get_page_serializer_class(value):
    return get_serializer_class(
        value.__class__,
        ['id', 'type', 'detail_url', 'html_url', 'title', 'slug'],
        meta_fields=['type', 'detail_url', 'html_url'],
        base=PageSerializer
    )


class PageListField(Field):
    """
    Serializes a list of Page objects.
    """
    def to_representation(self, value):
        if not value:
            return []

        serializer_class = get_page_serializer_class(value[0])
        serializer = serializer_class(context=self.context)

        return [
            serializer.to_representation(child_object)
            for child_object in value
        ]


class SiblingsField(PageListField):
    def get_attribute(self, instance):
        return instance.get_guide_siblings()


class ChildrenField(PageListField):
    def get_attribute(self, instance):
        return instance.get_live_children()


class PageParentField(WagtailPageParentField):
    """
    Like the Wagtail PageParentField but using a consistent page serializer.
    """
    def to_representation(self, value):
        serializer_class = get_page_serializer_class(value)
        serializer = serializer_class(context=self.context)
        return serializer.to_representation(value)


class PageSerializer(WagtailPageSerializer):
    parent = PageParentField(read_only=True)
    children = ChildrenField(read_only=True)
    siblings = SiblingsField(read_only=True)
    body = StreamField()
