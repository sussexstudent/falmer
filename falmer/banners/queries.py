import graphene

from . import models
from .types import Banner


class Query(graphene.ObjectType):
    all_active_banners = graphene.List(Banner)

    def resolve_all_active_banners(self, info):
        return models.Banner.objects.all_active()
