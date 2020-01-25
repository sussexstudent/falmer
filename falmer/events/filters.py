from django_filters import FilterSet, CharFilter, IsoDateTimeFilter, BooleanFilter, ModelChoiceFilter

from falmer.events.models import Curator
from . import models


class EventFilterSet(FilterSet):
    class Meta:
        model = models.Event
        fields = (
            'title',
            'venue',
            'type',
            'bundle',
            'parent',
            'brand',
            'student_group',
            'from_time',
            'to_time',

            'audience_just_for_pgs',
            'audience_suitable_kids_families',
            'audience_good_to_meet_people',
            'is_over_18_only',
            'cost',
            'alcohol',
            'type',
            'ticket_level',
            'curated_by'
        )

    title = CharFilter(lookup_expr='icontains')

    brand = CharFilter(field_name='brand__slug')
    bundle = CharFilter(field_name='bundle__slug')
    student_group = CharFilter(field_name='student_group__slug')

    to_time = IsoDateTimeFilter(field_name='start_time', lookup_expr='lte')

    from_time = IsoDateTimeFilter(field_name='end_time', lookup_expr='gte')
    uncurated = BooleanFilter(field_name='curated_by', lookup_expr='isnull')
    curated_by = ModelChoiceFilter(queryset=Curator.objects.all(), field_name='curated_by')
#
# class BrandingPeriodFilerSet(FilterSet):
#     class Meta:
#         model = BrandingPeriod
