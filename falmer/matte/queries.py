import graphene

from falmer.schema.schema import DjangoConnectionField
from . import types
from . import models

class Query(graphene.ObjectType):
    all_images = DjangoConnectionField(types.Image)
    image = graphene.Field(types.Image, media_id=graphene.Int())

    def resolve_all_images(self, info):
        if not info.context.user.has_perm('matte.can_list_all_matte_image'):
            raise PermissionError('not authorised to list images')
        qs = models.MatteImage.objects.all()

        return qs

    def resolve_image(self, info, **kwargs):
        media_id = kwargs.get('media_id')

        if not info.context.user.has_perm('matte.can_view_matte_image'):
            raise PermissionError('not authorised to view images')
        qs = models.MatteImage.objects.get(pk=media_id)

        return qs
