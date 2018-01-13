import graphene
from graphene_django import DjangoObjectType

from falmer.matte.types import Image
from falmer.schema.schema import create_connection
from . import models

class MSLStudentGroup(DjangoObjectType):
    logo = graphene.Field(Image)

    class Meta:
        model = models.MSLStudentGroup


class StudentGroup(DjangoObjectType):
    msl_group = graphene.Field(MSLStudentGroup)
    group_id = graphene.Int()

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


StudentGroup.Connection = create_connection(StudentGroup)
