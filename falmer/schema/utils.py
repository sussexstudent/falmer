import graphene


def create_connection(_node):
    class TotalCountConnection(graphene.Connection):
        total_count = graphene.Int()

        class Meta:
            name = _node._meta.name + 'Connection'
            node = _node

        def resolve_total_count(self, info):
            return self.length

    return TotalCountConnection
