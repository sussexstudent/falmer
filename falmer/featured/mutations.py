import graphene
from . import types
from . import models
from graphene.types.generic import GenericScalar


class SlateInput(graphene.InputObjectType):
    data = GenericScalar(required=True)


class UpdateSlate(graphene.Mutation):
    class Arguments:
        slate_id = graphene.Int(required=True)
        data = SlateInput(required=True)

    ok = graphene.Boolean()
    slate = graphene.Field(lambda: types.Slate)

    def mutate(self, info, slate_id, data):
        if not info.context.user.has_perm('featured.change_slate'):
            raise PermissionError()
        try:
            slate = models.Slate.objects.get(pk=slate_id)

            if 'data' in data:
                slate.data = data['data']

            slate.save()

            return UpdateSlate(ok=True, slate=slate)
        except DeprecationWarning as e:
            print(e)
            return UpdateSlate(ok=False, slate=None)


class Mutations(graphene.ObjectType):
    update_slate = UpdateSlate.Field()
