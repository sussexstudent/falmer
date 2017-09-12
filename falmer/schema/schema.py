from graphene_django import DjangoObjectType, DjangoConnectionField as _DjangoConnectionField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.rich_text import expand_db_html
from taggit.managers import TaggableManager
import graphene
from graphene_django.converter import convert_django_field
from falmer.auth import models as auth_models
from falmer.studentgroups import models as student_groups_models
from falmer.events import models as event_models
from falmer.matte.models import MatteImage


class DjangoConnectionField(_DjangoConnectionField):

    """
    Temporary fix for select_related issue
    """

    @classmethod
    def merge_querysets(cls, default_queryset, queryset):
        """
        This discarded all select_related and prefetch_related:
        # return default_queryset & queryset
        """
        return queryset

@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return "hello there"


@convert_django_field.register(TaggableManager)
def convert_taggable_manager(field, registry=None):
    return "hello there"


class Image(DjangoObjectType):
    resource = graphene.String()
    media_id = graphene.Int()

    def resolve_resource(self, args, context, info):
        return self.file.name

    def resolve_media_id(self, args, context, info):
        return self.pk

    class Meta:
        model = MatteImage
        interfaces = (graphene.relay.Node, )


class Venue(DjangoObjectType):

    class Meta:
        model = event_models.Venue


class Category(DjangoObjectType):

    class Meta:
        model = event_models.Category


class Type(DjangoObjectType):

    class Meta:
        model = event_models.Type


class BrandingPeriod(DjangoObjectType):

    class Meta:
        model = event_models.BrandingPeriod


class Bundle(DjangoObjectType):

    class Meta:
        model = event_models.Bundle


class Event(DjangoObjectType):
    venue = graphene.Field(Venue)
    featured_image = graphene.Field(Image)
    category = graphene.Field(Category)
    type = graphene.Field(Type)
    brand = graphene.Field(BrandingPeriod)
    bundle = graphene.Field(Bundle)
    body_html = graphene.String()
    event_id = graphene.Int()
    children = graphene.List(lambda: Event)
    parent = graphene.Field(lambda: Event)

    class Meta:
        model = event_models.Event
        interfaces = (graphene.relay.Node, )

    def resolve_body_html(self, args, context, info):
        return expand_db_html(self.body)

    def resolve_event_id(self, args, context, info):
        return self.pk

    def resolve_children(self, args, context, info):
        return self.children.all()

    def resolve_parent(self, args, context, info):
        return self.parent

class MSLStudentGroup(DjangoObjectType):
    logo = graphene.Field(Image)

    class Meta:
        model = student_groups_models.MSLStudentGroup


class StudentGroup(DjangoObjectType):
    msl_group = graphene.Field(MSLStudentGroup)
    group_id = graphene.Int()

    class Meta:
        model = student_groups_models.StudentGroup
        interfaces = (graphene.relay.Node, )

    def resolve_msl_group(self, args, context, info):
        try:
            return self.msl_group
        except student_groups_models.MSLStudentGroup.DoesNotExist:
            return None

    def resolve_group_id(self, args, context, info):
        return self.pk



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


class PageResult(graphene.ObjectType):
    pass


class SearchResult(graphene.Union):
    class Meta:
        types = (Event, StudentGroup)


class SearchResultConnection(graphene.Connection):
    class Meta:
        node = SearchResult


class EventFilter(graphene.InputObjectType):
    brand_id = graphene.Int()
    from_time = graphene.String()
    to_time = graphene.String()


class Query(graphene.ObjectType):
    all_events = DjangoConnectionField(Event, filter=graphene.Argument(EventFilter))
    event = graphene.Field(Event, event_id=graphene.Int())
    all_groups = DjangoConnectionField(StudentGroup)
    group = graphene.Field(StudentGroup, groupId=graphene.Int())

    all_images = DjangoConnectionField(Image)
    image = graphene.Field(Image, media_id=graphene.Int())
    # search = graphene.List(SearchResult)
    viewer = graphene.Field(ClientUser)
    search = graphene.ConnectionField(SearchResultConnection, query=graphene.String())

    def resolve_all_events(self, args, context, info):
        qs = event_models.Event.objects.select_related('featured_image', 'venue').prefetch_related('children').order_by('start_time')

        qfilter = args.get('filter')

        if qfilter is None:
            return qs

        if 'from_date' in qfilter:
            qs = qs.filter(end_time__gte=qfilter['from_time'])

        if 'to_time' in qfilter:
            qs = qs.filter(start_time__lte=qfilter['to_time'])

        if 'brand_id' in qfilter:
            qs = qs.filter(brand=qfilter['brand_id'])

        return qs

    def resolve_search(self, args, context, info):
        return [
            event_models.Event.objects.first(),
            student_groups_models.StudentGroup.objects.first(),
            student_groups_models.StudentGroup.objects.last(),
            event_models.Event.objects.last(),
        ]

    def resolve_event(self, args, context, info):
        return event_models.Event.objects.select_related('featured_image', 'bundle', 'brand').get(pk=args.get('event_id'))

    def resolve_all_groups(self, args, context, info):
        qs = student_groups_models.StudentGroup.objects\
            .order_by('name')\
            .select_related('msl_group', 'logo')

        return qs

    def resolve_all_images(self, args, context, info):
        if not context.user.has_perm('can_list_all'):
            raise PermissionError('not authorised to list images')
        qs = MatteImage.objects.all()

        return qs

    def resolve_image(self, args, context, info):
        if not context.user.has_perm('can_view'):
            raise PermissionError('not authorised to view images')
        qs = MatteImage.objects.get(pk=args.get('media_id'))

        return qs

    def resolve_group(self, args, context, info):
        return student_groups_models.StudentGroup.objects.select_related('logo').get(pk=args.get('groupId'))

    def resolve_viewer(self, args, context, info):
        if context.user.is_authenticated:
            return context.user
        return None

schema = graphene.Schema(query=Query)
