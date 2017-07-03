from graphene_django import DjangoObjectType
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailimages.models import Filter
from taggit.managers import TaggableManager
import graphene
from graphene_django.converter import convert_django_field
from falmer.auth import models as auth_models
from falmer.studentgroups import models as student_groups_models
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


class MSLStudentGroup(DjangoObjectType):
    logo = graphene.Field(Image)

    class Meta:
        model = student_groups_models.MSLStudentGroup


class StudentGroup(DjangoObjectType):
    msl_group = graphene.Field(MSLStudentGroup)

    class Meta:
        model = student_groups_models.StudentGroup

    def resolve_msl_group(self, args, context, info):
        try:
            return self.msl_group
        except student_groups_models.MSLStudentGroup.DoesNotExist:
            return None


class ClientUser(DjangoObjectType):
    name = graphene.String()
    has_cms_access = graphene.Boolean()

    class Meta:
        model = auth_models.FalmerUser

    def resolve_name(self, args, context, info):
        return self.get_full_name()

    # this is a quick hack until we work on permissions etc
    def resolve_has_cms_access(self, args, context, info):
        return self.has_perm('wagtailadmin.access_admin')


class SearchResult(graphene.Interface):
    pass


class Query(graphene.ObjectType):
    all_events = graphene.List(Event)
    # search = graphene.List(SearchResult)
    viewer = graphene.Field(ClientUser)
    all_groups = graphene.List(StudentGroup)

    def resolve_all_events(self, args, context, info):
        return event_models.Event.objects.all()\
            .select_related('featured_image')

    def resolve_all_groups(self, args, context, info):
        return student_groups_models.StudentGroup.objects.all()\
            .order_by('name')\
            .select_related('msl_group', 'msl_group__logo')

    def resolve_viewer(self, args, context, info):
        if context.user.is_authenticated:
            return context.user
        return None

schema = graphene.Schema(query=Query)
