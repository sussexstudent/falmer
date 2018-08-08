import graphene

from falmer.content.types import PageResult
from falmer.events.types import Event
from falmer.events import models as event_models
from falmer.studentgroups import models as studentgroup_models
from falmer.studentgroups.types import StudentGroup


class SearchResult(graphene.Union):
    class Meta:
        types = [Event, StudentGroup, PageResult]

    @classmethod
    def resolve_type(cls, instance, info):
        t = type(instance)

        if t == event_models.Event:
            return Event

        if t == studentgroup_models.StudentGroup:
            return StudentGroup

        return PageResult


class SearchResultConnection(graphene.Connection):
    class Meta:
        node = SearchResult


class SearchQuery(graphene.ObjectType):
    events = graphene.List(Event)
    content = graphene.List(PageResult)
    groups = graphene.List(StudentGroup)
    combined = graphene.List(graphene.String)
