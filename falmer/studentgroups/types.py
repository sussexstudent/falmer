from pprint import pprint

import graphene
from django.db.models import Prefetch
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


class Award(DjangoObjectType):
    class Meta:
        model = models.Award


class AwardAwarded(DjangoObjectType):
    class Meta:
        model = models.GroupAwarded


class AwardPeriod(DjangoObjectType):
    awarded = graphene.List(AwardAwarded)

    class Meta:
        model = models.AwardPeriod

    def resolve_awarded(self, info):
        return self.awards


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
        x = models.GroupAwarded.objects.select_related('award').filter(group=self)

        return models.AwardPeriod.objects.select_related('authority').prefetch_related(Prefetch('awarded', queryset=x, to_attr='awards')).filter(awarded__group=self).distinct()


StudentGroup.Connection = create_connection(StudentGroup)
