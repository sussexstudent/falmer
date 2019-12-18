import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from . import models


class Offer(DjangoObjectType):
    class Meta:
        model = models.Offer
        interfaces = (graphene.Node, )
        fields = (
            'id',
            'company_name',
            'company_logo',
            'company_website',
            'deal_tag',
            'is_featured',
            'category',
            'main',
        )

    main = GenericScalar()

    def resolve_main(self, info):
        return self.main.stream_block.get_api_representation(self.main, info.context)
