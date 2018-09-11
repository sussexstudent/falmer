from django_filters import FilterSet, CharFilter, IsoDateTimeFilter
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
            'ticket_level'
        )

    title = CharFilter(lookup_expr='icontains')

    brand = CharFilter(field_name='brand__slug')
    bundle = CharFilter(field_name='bundle__slug')

    to_time = IsoDateTimeFilter(field_name='start_time', lookup_expr='lte')

    from_time = IsoDateTimeFilter(field_name='end_time', lookup_expr='gte')
