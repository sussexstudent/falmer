import graphene

from falmer.schema.schema import DjangoConnectionField
from falmer.studentgroups.types import StudentGroup
from . import types
from . import models


class Query(graphene.ObjectType):
    all_groups = DjangoConnectionField(StudentGroup)
    group = graphene.Field(types.StudentGroup, group_id=graphene.Int())

    def resolve_all_groups(self, info):
        qs = models.StudentGroup.objects \
            .order_by('name') \
            .select_related('msl_group', 'logo')

        return qs

    def resolve_group(self, info, **kwargs):
        group_id = kwargs.get('group_id')

        return models.StudentGroup.objects \
            .select_related('logo').get(pk=group_id)
