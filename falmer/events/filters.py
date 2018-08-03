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
        )

    title = CharFilter(lookup_expr='icontains')

    brand = CharFilter(field_name='brand__slug')

    to_time = IsoDateTimeFilter(field_name='start_time', lookup_expr='lte')

    from_time = IsoDateTimeFilter(field_name='end_time', lookup_expr='gte')
