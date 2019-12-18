import graphene
from django.contrib.auth.models import Permission as DjangoPermission
from graphene_django import DjangoObjectType
from . import models


class ClientUser(DjangoObjectType):
    name = graphene.String()
    has_cms_access = graphene.Boolean()
    user_id = graphene.Int()
    permissions = graphene.List(graphene.Int)

    class Meta:
        model = models.FalmerUser
        fields = (
            'id',
            'name',
            'has_cms_access',
            'user_id',
            'permissions',
        )

    def resolve_name(self, info):
        return self.get_full_name()

    def resolve_user_id(self, info):
        return self.pk

    # this is a quick hack until we work on permissions etc
    def resolve_has_cms_access(self, info):
        return self.has_perm('wagtailadmin.access_admin')

    def resolve_permissions(self, info):
        return self.get_permissions()


class Permission(DjangoObjectType):
    content_type = graphene.String()

    class Meta:
        model = DjangoPermission
        fields = (
            'content_type',
        )

    def resolve_content_type(self, info):
        return self.content_type.app_label
