import graphene
import django_filters
from django.contrib.postgres.search import SearchVector

from falmer.schema.utils import NonNullDjangoConnectionField
from . import models
from . import types


class MarketListingsFilter(graphene.InputObjectType):
    q = graphene.String()
    section = graphene.String()
    own = graphene.Boolean()
    sort_by = graphene.String()


class ListingsFilter(django_filters.FilterSet):
    book_title = django_filters.CharFilter(lookup_expr='iexact')
    book_author = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.Listing
        fields = ['book_title', 'book_author']


class Query(graphene.ObjectType):
    all_market_listings = NonNullDjangoConnectionField(
        types.MarketListing,
        filters=graphene.Argument(MarketListingsFilter),
        required=True
    )

    all_market_sections = graphene.List(graphene.NonNull(types.MarketListingSection), required=True)

    market_listing = graphene.Field(types.MarketListing, listing_id=graphene.Int(required=True))
    market_section = graphene.Field(types.MarketListingSection, slug=graphene.String(required=True))

    def resolve_all_market_listings(self, info, **kwargs):
        qfilter = kwargs.get('filters')

        if 'own' in qfilter and qfilter['own'] is True:
            qs = models.Listing.objects.created_by(info.context.user)
        else:
            qs = models.Listing.objects.public()

        if 'q' in qfilter:
            qs = qs\
                .annotate(search=SearchVector('book_title', 'book_author'))\
                .filter(search=qfilter['q'])

        if 'section' in qfilter:
            qs = qs\
                .filter(section__slug=qfilter['section'])

        return qs.prefetch_related('images')

    def resolve_all_market_sections(self, info, **kwargs):
        return models.ListingSection.objects.order_by('title').all()

    def resolve_market_listing(self, info, **kwargs):
        listing_id = kwargs.get('listing_id')

        return models.Listing.objects.with_common().get_public_or_owned_by_user(
            pk=listing_id, user=info.context.user
        )

    def resolve_market_section(self, info, **kwargs):
        slug = kwargs.get('slug')

        return models.ListingSection.objects.get(
            slug=slug
        )
