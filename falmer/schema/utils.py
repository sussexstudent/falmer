import graphene
from graphene_django import DjangoConnectionField


def create_connection(_type):
    class Connection(graphene.Connection):
        total_count = graphene.Int()

        class Meta:
            name = _type._meta.name + 'ConnectionExt'
            node = _type

        class Edge(graphene.ObjectType):
            class Meta:
                name = _type._meta.name + 'EdgeX'
            node = graphene.Field(_type, required=True)
            cursor = graphene.String(required=True)

        def resolve_total_count(self, info):
            return self.length

        edges = graphene.List(graphene.NonNull(Edge), required=True)

    return Connection


class NonNullDjangoConnectionField(DjangoConnectionField):
    @property
    def type(self):
        ttype = super(graphene.ConnectionField, self).type

        try:
            return graphene.NonNull(self._type.of_type.Connection)
        except AttributeError:
            return graphene.NonNull(self._type)
        #print(self._type, type(self._type))
        #print(self._type.of_type, type(self._type.of_type))

    @classmethod
    def merge_querysets(cls, default_queryset, queryset):
        """
        This discarded all select_related and prefetch_related:
        # return default_queryset & queryset
        """
        return queryset
