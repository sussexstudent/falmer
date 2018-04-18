from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from . import models


class Offer(DjangoObjectType):
    class Meta:
        model = models.Offer

    main = GenericScalar()

    def resolve_main(self, info):
        return self.main.stream_block.get_api_representation(self.main, info.context)
