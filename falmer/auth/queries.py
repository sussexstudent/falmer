import graphene

from falmer.auth.types import ClientUser


class Query(graphene.ObjectType):
    viewer = graphene.Field(ClientUser)

    def resolve_viewer(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
