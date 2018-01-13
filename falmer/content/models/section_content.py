from django.db import models
from wagtail.api import APIField
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, StreamFieldPanel, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from falmer.content.blocks import ContactBlock, SectionBlock
from falmer.content.serializers import WagtailImageSerializer
from falmer.matte.models import MatteImage


class SectionContentPage(Page):
    body = StreamField([
        ('section', SectionBlock()),
    ])

    content_panels = Page.content_panels + [
        ImageChooserPanel('heading_image'),
        StreamFieldPanel('body'),
    ]

    contents_in_sidebar = models.BooleanField(default=True)
    heading_image = models.ForeignKey(MatteImage, null=True, blank=False, on_delete=models.SET_NULL)

    sidebar_body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('contact', ContactBlock()),
    ], blank=True)

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

    api_fields = (
        'body',
        'sidebar_body',
        'contents_in_sidebar',
        'heading_image',
    )
