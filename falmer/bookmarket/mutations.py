import graphene

from falmer.matte.models import MatteImage
from . import types
from . import models


class MarketListingInput(graphene.InputObjectType):
    book_title = graphene.String(required=True)
    book_author = graphene.String(required=True)
    description = graphene.String(required=True)
    contact_details = graphene.String(required=True)
    price = graphene.Float(required=True)
    section_id = graphene.Int(required=True)


class MarketListingUpdateInput(MarketListingInput):
    book_title = graphene.String()
    book_author = graphene.String()
    description = graphene.String()
    contact_details = graphene.String()
    price = graphene.Float()
    section_id = graphene.Int()
    state = graphene.String()
    image_id = graphene.Int()


class CreateMarketListing(graphene.Mutation):
    class Arguments:
        listing_data = MarketListingInput(required=True)

    ok = graphene.Boolean()
    listing = graphene.Field(lambda: types.MarketListing)

    def mutate(self, info, listing_data):
        print(info.context.user)
        if info.context.user is None:
            raise PermissionError('not logged in')
            return CreateMarketListing(ok=False, listing=None)

        try:
            listing = models.Listing.objects.create(
                book_title=listing_data.book_title,
                book_author=listing_data.book_author,
                description=listing_data.description,
                contact_details=listing_data.contact_details,
                listing_user=info.context.user,
                section_id=listing_data.section_id,
                buy_price=listing_data.price,
                state='DRAFT',
            )

            return CreateMarketListing(ok=True, listing=listing)
        except DeprecationWarning as e:
            print(e)
            return CreateMarketListing(ok=False, listing=None)


class UpdateMarketListing(graphene.Mutation):
    class Arguments:
        listing_id = graphene.Int()
        listing_data = MarketListingUpdateInput(required=True)

    ok = graphene.Boolean()
    listing = graphene.Field(lambda: types.MarketListing)

    def mutate(self, info, listing_id, listing_data):

        listing = models.Listing.objects.get_owned_by_user(listing_id=listing_id, owner=info.context.user)

        try:
            if 'book_title' in listing_data:
                listing.book_title = listing_data['book_title']

            if 'book_author' in listing_data:
                listing.book_author = listing_data['book_author']

            if 'price' in listing_data:
                listing.buy_price = listing_data['price']

            if 'description' in listing_data:
                listing.description = listing_data['description']

            if 'contact_details' in listing_data:
                listing.contact_details = listing_data['contact_details']

            if 'section_id' in listing_data:
                listing.section_id = listing_data['section_id']

            if 'state' in listing_data:
                listing.transition_state(listing_data['state'])

            if 'image_id' in listing_data:
                try:
                    image = MatteImage.objects.get(pk=listing_data['image_id'])
                    listing.images.clear()
                    listing.images.add(image)
                except:
                    raise RuntimeWarning('failed to add')

            listing.save()

            return UpdateMarketListing(ok=True, listing=listing)
        except DeprecationWarning as e:
            print(e)
            return UpdateMarketListing(ok=False, listing=None)

# ChangeBookListingStatus


class RequestDetails(graphene.Mutation):
    class Arguments:
        listing_id = graphene.Int()

    listing = graphene.Field(types.MarketListing)

    def mutate(self, info, listing_id):
        listing = models.Listing.objects.public().get(pk=listing_id)

        listing.record_request(info.context.user)

        return RequestDetails(listing=listing)


class Mutations(graphene.ObjectType):
    create_market_listing = CreateMarketListing.Field()
    update_market_listing = UpdateMarketListing.Field()
    request_market_listing_contact_details = RequestDetails.Field()
