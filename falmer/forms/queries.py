import graphene
from . import models
from . import types

class Query(graphene.ObjectType):
    consent_form = graphene.Field(types.ConsentCodeForm, slug=graphene.String())

    def resolve_consent_form(self, info, **kwargs):
        return models.ConsentCodeForm.objects.get(slug=kwargs.get('slug'))
