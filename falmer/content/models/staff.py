from django.db import models
from wagtail.wagtailimages import get_image_model_string
from modelcluster.fields import ParentalKey
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel


@register_snippet
class StaffMemberSnippet(index.Indexed, models.Model):
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    office_phone_number = models.CharField(max_length=255, null=True, blank=True)
    mobile_phone_number = models.CharField(max_length=255, null=True, blank=True)
    job_description = RichTextField(default='', blank=True)
    office_location = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('job_title'),
        FieldPanel('email'),
        FieldPanel('office_phone_number'),
        FieldPanel('mobile_phone_number'),
        ImageChooserPanel('photo'),
        FieldPanel('job_description'),
    ]

    search_fields = [
        index.SearchField('name', partial_match=True),
        index.SearchField('job_title', partial_match=True),
    ]

    def __str__(self):
        return self.name


class StaffMemberChooser(SnippetChooserBlock):
    def get_api_representation(self, value, context=None):
        from falmer.content.serializers import SnippetSerializer
        return SnippetSerializer(instance=value).data


class StaffListBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    body = blocks.ListBlock(StaffMemberChooser(StaffMemberSnippet))

    class Meta:
        icon = 'user'


class StaffPage(Page):
    parent_page_types = ('wagtailcore.Page', )
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('staff_list', StaffListBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    api_fields = (
        'body',
    )




class StaffDepartment(Page):
    subpage_types = ('StaffSection',)


class StaffSection(Page):
    content_panels = Page.content_panels + [
        InlinePanel('staff', label="Staff"),
    ]


class StaffMember(Orderable):
    department = ParentalKey(StaffSection, related_name='staff')
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    office_phone_number = models.CharField(max_length=255, null=True, blank=True)
    mobile_phone_number = models.CharField(max_length=255, null=True, blank=True)
    job_description = RichTextField()
    office_location = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('job_title'),
        FieldPanel('email'),
        FieldPanel('office_phone_number'),
        FieldPanel('mobile_phone_number'),
        ImageChooserPanel('photo'),
        FieldPanel('job_description'),
    ]

