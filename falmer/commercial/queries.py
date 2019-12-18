import graphene
from .models import Offer
from . import types


class Query(graphene.ObjectType):
    all_offers = graphene.List(graphene.NonNull(types.Offer), required=True)

    def resolve_all_offers(self, info):
        return Offer.objects.order_by('company_name').all()
