import arrow
import graphene
from django.db.models import Q
from django.utils import timezone

from falmer.events.filters import EventFilterSet
from falmer.events.types import Venue, BrandingPeriod, Event, Bundle
from falmer.schema.fields import FalmerDjangoFilterConnectionField
from falmer.schema.schema import DjangoConnectionField
from . import models


class Query(graphene.ObjectType):
    # all_events = DjangoConnectionField(Event, filter=graphene.Argument(EventFilter))
    all_events = FalmerDjangoFilterConnectionField(Event, filterset_class=EventFilterSet, brand=graphene.String(), skip_embargo=graphene.Boolean())
    all_venues = DjangoConnectionField(Venue)
    event = graphene.Field(Event, event_id=graphene.Int(), msl_event_id=graphene.Int())
    branding_period = graphene.Field(BrandingPeriod, slug=graphene.String())
    bundle = graphene.Field(Bundle, slug=graphene.String())

    def resolve_all_events(self, info, **kwargs):
        qfilter = kwargs.get('filter')

        qs = models.Event.objects.select_related('featured_image', 'venue', 'mslevent') \
            .prefetch_related('children').order_by('start_time', 'end_time')

        if qfilter is None:
            return qs.filter(parent=None)

        if 'include_children' in qfilter:
            pass
        else:
            qs = qs.filter(parent=None)

        if kwargs.get('skip_embargo', False):
            pass
        else:
            qs = qs.filter(Q(embargo_until=None) | Q(embargo_until__lte=timezone.now()))

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
