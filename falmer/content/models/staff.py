from django.db import models
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, HelpPanel, MultiFieldPanel
from .core import Page


@register_snippet
class StaffMemberSnippet(index.Indexed, models.Model):
    class Meta:
        verbose_name = 'Job Role'
        verbose_name_plural = 'Job Roles'

    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, null=True, blank=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    office_phone_number = models.CharField(max_length=255, null=True, blank=True)
    mobile_phone_number = models.CharField(max_length=255, null=True, blank=True)
    job_description = RichTextField(default='', blank=True)
    office_location = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        HelpPanel('Humans should be assigned to the job role. If a person has switched roles, please update snippet of their new role with their infomation, rather than updating their current role snippet with their new role.'),
        MultiFieldPanel((
            FieldPanel('name'),
            FieldPanel('mobile_phone_number'),
            ImageChooserPanel('photo'),
            FieldPanel('email'),
        ), heading='Employee centric details'),
        MultiFieldPanel((
            FieldPanel('job_title'),
            FieldPanel('job_description'),
            FieldPanel('office_phone_number'),
        ), heading='Role centric details', help_text='These should not need to change'),
    ]

    search_fields = [
        index.SearchField('job_title', partial_match=True, boost=1.1),
        index.SearchField('name', partial_match=True),
    ]

    def __str__(self):
        return f'{self.job_title} ({self.name})'


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

