import graphene
from graphene_django import DjangoObjectType

from falmer.schema.utils import NonNullDjangoConnectionField, create_connection
from . import models


class ImageLabel(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self.label.name

    class Meta:
        model = models.ImageLabelThrough
        interfaces = (graphene.Node, )
        fields = ()


ImageLabel.Connection = create_connection(ImageLabel)


class Image(DjangoObjectType):
    resource = graphene.String(required=True)
    media_id = graphene.Int(required=True)
    #labels = NonNullDjangoConnectionField(ImageLabel, required=True)

    def resolve_resource(self, info):
        return self.file.name

    def resolve_media_id(self, info):
        return self.pk

    class Meta:
        model = models.MatteImage
        interfaces = (graphene.Node, )
        fields = (
            'labels',
            'width',
            'height',
        )


Image.Connection = create_connection(Image)
