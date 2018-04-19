import graphene
from .models import Flag
from . import types


class Query(graphene.ObjectType):
    all_flags = graphene.List(types.Flag)

    def resolve_all_flags(self, info):
        return Flag.objects.filter(expired=False)
