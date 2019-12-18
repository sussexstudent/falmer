import graphene
from .models import Flag
from . import types


class Query(graphene.ObjectType):
    all_flags = graphene.List(graphene.NonNull(types.Flag), required=True)

    def resolve_all_flags(self, info):
        return Flag.objects.filter(expired=False)
