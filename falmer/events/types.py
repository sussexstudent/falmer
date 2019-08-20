import graphene
from graphene_django import DjangoObjectType
from wagtail.core.rich_text import expand_db_html
from falmer.matte.types import Image
from falmer.schema.schema import File
from falmer.schema.utils import create_connection
from falmer.studentgroups.types import StudentGroup
from . import models

class PAValues(graphene.Enum):
    NA = 0
    NEGATIVE = 1
    POSITIVE = 2


class BrandingPeriodFilter(graphene.InputObjectType):
    from_time = graphene.String()
    to_time = graphene.String()
    ignore_time_if_archived = graphene.Boolean()


class EventFilter(graphene.InputObjectType):
    brand_slug = graphene.String()
    from_time = graphene.String()
    to_time = graphene.String()


class Venue(DjangoObjectType):
    venue_id = graphene.Int()

    class Meta:
        model = models.Venue
        interfaces = (graphene.Node, )

    def resolve_venue_id(self, info):
        return self.pk


class Category(DjangoObjectType):

    class Meta:
        model = models.Category


class CategoryNode(DjangoObjectType):
    parent = graphene.Field(lambda: CategoryNode)

    class Meta:
        model = models.CategoryNode

    def resolve_parent(self, info):
        return self.get_parent()


class Type(DjangoObjectType):

    class Meta:
        model = models.Type


class BrandingPeriod(DjangoObjectType):
    logo_vector = graphene.Field(File)

    class Meta:
        model = models.BrandingPeriod

    def resolve_logo_vector(self, info):
        if bool(self.logo_vector) is False:
            return None
        return self.logo_vector


class Bundle(DjangoObjectType):

    class Meta:
        model = models.Bundle


class MSLEvent(DjangoObjectType):
    class Meta:
        model = models.MSLEvent
        interfaces = (graphene.Node, )


class Curator(DjangoObjectType):
    class Meta:
        model = models.Curator


class EventLike(DjangoObjectType):
    class Meta:
        model = models.EventLike


class Event(DjangoObjectType):
    venue = graphene.Field(Venue)
    featured_image = graphene.Field(Image)
    categories = graphene.List(CategoryNode)
    type = graphene.Field(Type)
    brand = graphene.Field(BrandingPeriod)
    bundle = graphene.Field(Bundle)
    student_group = graphene.Field(lambda: StudentGroup)
    body_html = graphene.String()
    event_id = graphene.Int()
    children = graphene.List(lambda: Event)
    parent = graphene.Field(lambda: Event)
    msl_event_id = graphene.Int()
    msl_event = graphene.Field(lambda: MSLEvent)
    user_like = graphene.Field(EventLike)

    class Meta:
        model = models.Event
        interfaces = (graphene.Node, )

    def resolve_user_like(self, info):
        info.context.loaders.event_like.load(self.pk)

    def resolve_body_html(self, info):
        return expand_db_html(self.body)

    def resolve_event_id(self, info):
        return self.pk

    def resolve_msl_event_id(self, info):
        return self.get_msl_event_id()

    def resolve_msl_event(self, info):
        try:
            return self.mslevent
        except models.MSLEvent.DoesNotExist:
            return None

    def resolve_student_group(self, info):
        return self.student_group

    def resolve_categories(self, info):
        return self.category.all()

    def resolve_children(self, info):
        return self.children.all()

    def resolve_parent(self, info):
        return self.parent


Event.Connection = create_connection(Event)
