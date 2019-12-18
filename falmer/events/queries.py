import arrow
import graphene
from django.db.models import Q, Count
from django.utils import timezone

from falmer.events.filters import EventFilterSet
from falmer.events.types import Venue, BrandingPeriod, Event, Bundle
from falmer.schema.fields import FalmerDjangoFilterConnectionField
from falmer.schema.utils import NonNullDjangoConnectionField
from . import models


class Query(graphene.ObjectType):
    # all_events = DjangoConnectionField(Event, filter=graphene.Argument(EventFilter))
    all_events = FalmerDjangoFilterConnectionField(Event, filterset_class=EventFilterSet, brand=graphene.String(), skip_embargo=graphene.Boolean(), viewer_liked=graphene.Boolean(), required=True)
    all_venues = NonNullDjangoConnectionField(Venue, required=True)
    all_branding_periods = graphene.Field(graphene.List(graphene.NonNull(BrandingPeriod)), required=True)
    event = graphene.Field(Event, event_id=graphene.Int(), msl_event_id=graphene.Int(), required=True)
    branding_period = graphene.Field(BrandingPeriod, slug=graphene.String(required=True), required=True)
    bundle = graphene.Field(Bundle, slug=graphene.String(required=True), required=True)

    def resolve_all_events(self, info, **kwargs):
        qfilter = kwargs.get('filter')

        qs = models.Event.objects.select_related('featured_image', 'venue', 'mslevent') \
            .prefetch_related('children').order_by('start_time', 'end_time')

        if kwargs.get('skip_embargo', False):
            pass
        else:
            qs = qs.filter(Q(embargo_until=None) | Q(embargo_until__lte=timezone.now()))

        if kwargs.get('viewer_liked', False) and info.context.user.is_authenticated:
            qs = qs.filter(Q(eventlike__user=info.context.user) & Q(eventlike__source='USER'))

        if qfilter is None:
            print('returning')
            return qs.filter(parent=None)

        if 'include_children' in qfilter:
            pass
        else:
            qs = qs.filter(parent=None)

        if 'from_time' in qfilter:
            qs = qs.filter(end_time__gte=qfilter['from_time'])

        if 'to_time' in qfilter:
            qs = qs.filter(start_time__lte=qfilter['to_time'])

        if 'brand' in qfilter:
            pass
        else:
            qs = qs.filter(
                Q(mslevent__last_sync__gte=arrow.now().shift(minutes=-30).datetime) | Q(mslevent__isnull=True)
            )

        return qs

    def resolve_branding_period(self, info, **kwargs):
        slug = kwargs.get('slug')
        return models.BrandingPeriod.objects.get(slug=slug)

    def resolve_bundle(self, info, **kwargs):
        slug = kwargs.get('slug')
        return models.Bundle.objects.get(slug=slug)

    def resolve_all_venues(self, info):
        return models.Venue.objects.all()

    def resolve_all_branding_periods(self, info):
        periods = models.BrandingPeriod.objects \
            .annotate(events_count=Count('events')) \
            .filter(display_from__lte=timezone.now())
        return periods

    def resolve_event(self, info, **kwargs):
        event_id = kwargs.get('event_id')
        msl_event_id = kwargs.get('msl_event_id')
        if event_id is not None:
            return models.Event.objects.select_related(
                'featured_image',
                'bundle',
                'brand',
                'student_group'
            ).get(pk=event_id)

        if msl_event_id is not None:
            return models.MSLEvent.objects.get(msl_event_id=msl_event_id).event

        return None
