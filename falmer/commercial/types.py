from graphene_django import DjangoObjectType
from . import models


class Offer(DjangoObjectType):
    class Meta:
        model = models.Offer
