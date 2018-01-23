import graphene
from . import models
from . import types


class Query(graphene.ObjectType):
    knowledge_base = graphene.Field(types.KnowledgeBase)

    def resolve_knowledge_base(self, info, **kwargs):
        return models.KnowledgeBaseRoot.objects.first()
