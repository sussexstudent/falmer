from graphene_django import DjangoObjectType

from . import models


class Banner(DjangoObjectType):
    class Meta:
        model = models.Banner
        fields = (
            'id',
            'outlet',
            'display_from',
            'display_to',
            'purpose',
            'heading',
            'body',
        )
