from django.conf import settings
from django.db import models
from django.urls import reverse
from rest_framework import serializers
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages import get_image_model_string
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, StreamFieldPanel, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet

from falmer.matte.models import MatteImage


def generate_image_url(image, filter_spec):
    from wagtail.wagtailimages.views.serve import generate_signature
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    # Append image's original filename to the URL (optional)
    # url += image.file.name[len('original_images/'):]

    return settings.PUBLIC_HOST + url

@register_snippet
class StaffMemberSnippet(models.Model):
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

    def __str__(self):
        return self.name


class WagtailImageSerializer(serializers.ModelSerializer):
    resource_url = serializers.SerializerMethodField()

    class Meta:
        model = MatteImage
        fields = ('id', 'resource_url')

    def get_resource_url(self, image):
        return generate_image_url(image, 'fill-400x400')


class SnippetSerializer(serializers.ModelSerializer):
    photo = WagtailImageSerializer()

    class Meta:
        model = StaffMemberSnippet
        fields = ('name', 'job_title', 'email', 'office_phone_number', 'mobile_phone_number', 'job_description', 'office_location', 'photo')

class StaffMemberChooser(SnippetChooserBlock):
    def get_api_representation(self, value, context=None):
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


class ContactBlock(blocks.StructBlock):
    body = blocks.TextBlock()
    name = blocks.CharBlock()
    email = blocks.EmailBlock()

    class Meta:
        icon = 'user'


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
    ])

    class Meta:
        icon = 'user'


class SectionContentPage(Page):
    body = StreamField([
        ('section', SectionBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    contents_in_sidebar = models.BooleanField(default=True)

    sidebar_body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('contact', ContactBlock()),
    ])


    sidebar_content_panels = [
        FieldPanel('contents_in_sidebar'),
        StreamFieldPanel('sidebar_body'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_content_panels, heading='Sidebar content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
