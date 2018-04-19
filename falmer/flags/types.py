from graphene_django import DjangoObjectType
from . import models


class Flag(DjangoObjectType):
    class Meta:
        model = models.Flag
