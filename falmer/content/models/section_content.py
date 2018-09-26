from django.db import models
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, StreamFieldPanel, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel

from falmer.content.blocks import ContactBlock, SectionBlock, RichTextWithExpandedContent
from falmer.content.models.core import Page
from falmer.matte.models import MatteImage


class SectionContentPage(Page):
    parent_page_types = []

    body = StreamField([
        ('section', SectionBlock()),
    ])

    content_panels = Page.content_panels + [
        ImageChooserPanel('heading_image'),
        StreamFieldPanel('body'),
    ]

    contents_in_sidebar = models.BooleanField(default=True)
    heading_image = models.ForeignKey(MatteImage, null=True, blank=False, on_delete=models.SET_NULL)
    heading_image_as_hero = models.BooleanField(default=False)

    sidebar_body = StreamField([
        ('paragraph', RichTextWithExpandedContent()),
        ('contact', ContactBlock()),
    ], blank=True)

    sidebar_content_panels = [
        FieldPanel('contents_in_sidebar'),
        FieldPanel('heading_image_as_hero'),
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
        'heading_image_as_hero',
        'heading_image',
    )
