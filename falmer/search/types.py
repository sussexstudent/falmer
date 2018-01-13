class Query(graphene.ObjectType):
    search = graphene.ConnectionField(SearchResultConnection, query=graphene.String())

    def resolve_search(self, info):
        return [
            event_models.Event.objects.first(),
            student_groups_models.StudentGroup.objects.first(),
            student_groups_models.StudentGroup.objects.last(),
            event_models.Event.objects.last(),
        ]
