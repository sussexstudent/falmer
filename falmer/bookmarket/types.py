import graphene
from graphene_django import DjangoObjectType

from falmer.auth.models import FalmerUser
from falmer.matte.types import Image
from falmer.schema.utils import create_connection
from . import models

MarketListingState = graphene.Enum('MarketListingState', [
    (models.LISTING_STATE_DRAFT, models.LISTING_STATE_DRAFT),
    (models.LISTING_STATE_READY, models.LISTING_STATE_READY),
    (models.LISTING_STATE_UNLISTED, models.LISTING_STATE_UNLISTED),
    (models.LISTING_STATE_EXPIRED, models.LISTING_STATE_EXPIRED),
])


class PublicUser(DjangoObjectType):
    user_id = graphene.Int(required=True)

    class Meta:
        model = FalmerUser
        fields = ('id', 'name')

    def resolve_user_id(self, info):
        return self.pk


class MarketListing(DjangoObjectType):
    pk = graphene.Int(required=True)
    image = graphene.Field(Image)
    listing_user = graphene.Field(PublicUser, required=True)
    contact_details = graphene.String()
    state = graphene.Field(MarketListingState, required=True)

    class Meta:
        model = models.Listing
        interfaces = (graphene.Node, )
        fields = (
            'id',
            'listing_user',
            'contact_details',
            'book_title',
            'book_author',
            'description',
            'section',
            'buy_price',
            'state',
            'listed_at',
            'images',
        )
        filter_fields = ['section', 'book_title', 'book_author']

    def resolve_pk(self, info):
        return self.pk

    def resolve_image(self, info):
        return self.featured_image()

    def resolve_listing_user(self, info):
        return self.listing_user

    def resolve_contact_details(self, info):
        if not info.context.user.is_authenticated or not self.can_see_contact_details(info.context.user):
            return None
        else:
            return self.contact_details

MarketListing.Connection = create_connection(MarketListing)


class MarketListingSection(DjangoObjectType):
    class Meta:
        model = models.ListingSection
        fields = (
            'id',
            'title',
            'slug'
        )

    pk = graphene.Int(required=True)

    def resolve_pk(self, info):
        return self.pk
