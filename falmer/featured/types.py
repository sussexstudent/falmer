import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from falmer.schema.utils import create_connection
from . import models


class Slate(DjangoObjectType):
    data = GenericScalar()
    enhanced_data = GenericScalar()
    slate_id = graphene.Int()

    class Meta:
        model = models.Slate
        interfaces = (graphene.Node, )
        only_fields = (
            'id',
            'data',
            'display_from',
            'notes'
        )

    def resolve_data(self, info):
        return self.data

    def resolve_enhanced_data(self, info):
        return self.enhanced_data()

    def resolve_slate_id(self, info):
        return self.pk


Slate.connection = create_connection(Slate)
