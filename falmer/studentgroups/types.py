import graphene
from graphene_django import DjangoObjectType

from falmer.matte.types import Image
from falmer.schema.schema import create_connection
from . import models


class MSLStudentGroup(DjangoObjectType):
    logo = graphene.Field(Image)

    class Meta:
        model = models.MSLStudentGroup


class AwardAuthority(DjangoObjectType):
    class Meta:
        model = models.AwardAuthority


class AwardPeriod(DjangoObjectType):
    class Meta:
        model = models.AwardPeriod


class Award(DjangoObjectType):
    class Meta:
        model = models.Award


class AwardAwarded(DjangoObjectType):
    class Meta:
        model = models.GroupAwarded


class StudentGroup(DjangoObjectType):
    msl_group = graphene.Field(MSLStudentGroup)
    group_id = graphene.Int()
    awards = graphene.List(AwardPeriod)

    class Meta:
        model = models.StudentGroup
        interfaces = (graphene.Node, )

    def resolve_msl_group(self, info):
        try:
            return self.msl_group
        except models.MSLStudentGroup.DoesNotExist:
            return None

    def resolve_group_id(self, info):
        return self.pk

    def resolve_awards(self, info):
        return models.AwardPeriod.objects.filter(awarded__group=self).select_related('authority').prefetch_related('awarded', 'awarded__award').distinct()


StudentGroup.Connection = create_connection(StudentGroup)
