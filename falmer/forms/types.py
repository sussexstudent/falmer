import graphene
from graphene_django import DjangoObjectType
from . import models

class ConsentCodeForm(DjangoObjectType):

    class Meta:
        model = models.ConsentCodeForm



class ConsentCodeAuthorisation(DjangoObjectType):

    class Meta:
        model = models.ConsentCodeAuthorisation
