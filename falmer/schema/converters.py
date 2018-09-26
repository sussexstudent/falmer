import graphene
from graphene_django.converter import convert_django_field
from wagtail.core.fields import RichTextField
from wagtail.core.rich_text import expand_db_html

from falmer.content.utils import change_dict_naming_convention, underscore_to_camel


class GenericStreamFieldType(graphene.Scalar):
    @staticmethod
    def serialize(stream_value):
        return change_dict_naming_convention(stream_value.stream_block.get_api_representation(stream_value), underscore_to_camel)


class RichTextFieldType(graphene.String):
    @staticmethod
    def serialize(value):
        return expand_db_html(value.source)


class FalmerFile(graphene.ObjectType):
    url = graphene.String()

def register_converters():
    from django.db import models
    from taggit.managers import TaggableManager
    from wagtail.core.fields import StreamField

    @convert_django_field.register(StreamField)
    def convert_stream_field(field, registry=None):
        return GenericStreamFieldType(
            description=field.help_text, required=not field.null
        )

    @convert_django_field.register(RichTextField)
    def convert_rich_text_field(field, registry=None):
        return RichTextFieldType(
            description=field.help_text, required=not field.null
        )


    @convert_django_field.register(TaggableManager)
    def convert_taggable_manager(field, registry=None):
        return "hello there"


    @convert_django_field.register(models.FileField)
    def convert_stream_field(field, registry=None):
        return graphene.Field(
            FalmerFile,
            description=field.help_text, required=not field.null
        )
