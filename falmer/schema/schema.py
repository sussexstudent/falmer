from graphene_django import DjangoObjectType
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailimages.models import Image, Filter
from taggit.managers import TaggableManager
import graphene
from graphene_django.converter import convert_django_field
from falmer.content.models import StaffPage, StaffMember, StaffDepartment, StaffSection


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    return "hello there"


@convert_django_field.register(TaggableManager)
def convert_taggable_manager(field, registry=None):
    return "hello there"


class WagtailImage(DjangoObjectType):
    url = graphene.String(width=graphene.Int())

    def resolve_url(self, args, context, info):
        filter = Filter()
        filter.spec = 'width-{}'.format(args.get('width'))
        return self.get_rendition(filter).url

    class Meta:
        model = Image


class StaffType(DjangoObjectType):
    class Meta:
        model = StaffMember


class StaffSectionType(DjangoObjectType):
    class Meta:
        model = StaffSection


class StaffDepartmentType(DjangoObjectType):
    sections = graphene.List(StaffSectionType)

    def resolve_sections(self, args, content, info):
        return self.get_children().live().type(StaffSection).specific()

    class Meta:
        model = StaffDepartment


class StaffPageType(DjangoObjectType):
    departments = graphene.List(StaffDepartmentType)

    def resolve_departments(self, args, content, info):
        r = self.get_children().live().type(StaffDepartment).specific()
        return r

    class Meta:
        model = StaffPage



class Query(graphene.ObjectType):
    staff = graphene.Field(StaffPageType)

    def resolve_staff(self, args, context, info):
        # hacky - TODO: investigate better way of having 'singleton' pages, via slug perhaps?
        return StaffPage.objects.all()[0];


schema = graphene.Schema(query=Query)
