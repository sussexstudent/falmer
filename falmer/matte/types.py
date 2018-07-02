import graphene
from graphene_django import DjangoObjectType

from falmer.schema.schema import DjangoConnectionField, create_connection
from . import models

class ImageLabel(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self.label.name

    class Meta:
        model = models.ImageLabelThrough
        interfaces = (graphene.Node, )


class Image(DjangoObjectType):
    resource = graphene.String()
    media_id = graphene.Int()
    labels = DjangoConnectionField(ImageLabel)

    def resolve_resource(self, info):
        return self.file.name

    def resolve_media_id(self, info):
        return self.pk

    class Meta:
        model = models.MatteImage
        interfaces = (graphene.Node, )


Image.Connection = create_connection(Image)
