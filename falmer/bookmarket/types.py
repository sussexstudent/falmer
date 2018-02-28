import graphene
from graphene_django import DjangoObjectType

from falmer.auth.models import FalmerUser
from falmer.matte.types import Image
from falmer.schema.schema import create_connection
from . import models


class PublicUser(DjangoObjectType):
    user_id = graphene.Int()

    class Meta:
        model = FalmerUser
        only_fields = ('id', 'name')

    def resolve_user_id(self, info):
        return self.pk


class MarketListing(DjangoObjectType):
    pk = graphene.Int()
    image = graphene.Field(Image)
    listing_user = graphene.Field(PublicUser)

    class Meta:
        model = models.Listing
        interfaces = (graphene.Node, )
        filter_fields = ['section', 'book_title', 'book_author']

    def resolve_pk(self, info):
        return self.pk

    def resolve_image(self, info):
        return self.featured_image()

    def resolve_listing_user(self, info):
        return self.listing_user


MarketListing.connection = create_connection(MarketListing)


class MarketListingSection(DjangoObjectType):
    class Meta:
        model = models.ListingSection

    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk
