from graphene_django import DjangoObjectType
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailimages.models import Filter
from taggit.managers import TaggableManager
import graphene
from graphene_django.converter import convert_django_field
from falmer.events import models as event_models
from falmer.matte.models import MatteImage


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return "hello there"


@convert_django_field.register(TaggableManager)
def convert_taggable_manager(field, registry=None):
    return "hello there"


class Image(DjangoObjectType):
    resource = graphene.String()

    def resolve_resource(self, args, context, info):
        return self.file.name

    class Meta:
        model = MatteImage


class Venue(DjangoObjectType):

    class Meta:
        model = event_models.Venue


class Event(DjangoObjectType):
    venue = graphene.Field(Venue)
    featured_image = graphene.Field(Image)

    class Meta:
        model = event_models.Event


class Query(graphene.ObjectType):
    all_events = graphene.List(Event)

    def resolve_all_events(self, args, context, info):
        return event_models.Event.objects.all()


schema = graphene.Schema(query=Query)
