import graphene

from falmer.events.types import Event
from falmer.studentgroups.types import StudentGroup


class PageResult(graphene.ObjectType):
    pass


class SearchResult(graphene.Union):
    class Meta:
        types = (Event, StudentGroup)


class SearchResultConnection(graphene.Connection):
    class Meta:
        node = SearchResult
