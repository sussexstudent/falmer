import graphene
from . import types
from . import models

class AcceptConsentForm(graphene.Mutation):
    class Arguments:
        slug = graphene.String()

    authorisation = graphene.Field(types.ConsentCodeAuthorisation)

    def mutate(self, info, slug):
        form = models.ConsentCodeForm.objects.get(slug=slug)

        authorisation = form.accept_for(info.context.user)

        return AcceptConsentForm(authorisation=authorisation)


class Mutations(graphene.ObjectType):
    accept_consent = AcceptConsentForm.Field()
