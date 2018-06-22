import graphene
import arrow
from django.db.models import Q
from falmer.schema.schema import DjangoConnectionField
from falmer.studentgroups.types import StudentGroup
from . import types
from . import models


class Query(graphene.ObjectType):
    all_groups = DjangoConnectionField(StudentGroup)
    group = graphene.Field(types.StudentGroup, group_id=graphene.Int(), group_slug=graphene.String())

    def resolve_all_groups(self, info):
        qs = models.StudentGroup.objects \
            .order_by('name') \
            .select_related('msl_group', 'logo') \
            .filter(Q(msl_group__last_sync__gte=arrow.now().shift(minutes=-90).datetime) | Q(msl_group__isnull=True))

        return qs

    def resolve_group(self, info, **kwargs):
        group_slug = kwargs.get('group_slug')
        group_id = kwargs.get('group_id')

        if group_slug:
            return models.StudentGroup.objects \
                .select_related('logo').get(slug=group_slug)
        if group_id:
            return models.StudentGroup.objects \
                .select_related('logo').get(pk=group_id)

        return None
