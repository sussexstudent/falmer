from django.db import models
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, StreamFieldPanel, ObjectList
from wagtail.wagtailimages import get_image_model_string
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from falmer.content.blocks import HeroImageBlock, ImageBlock


class GridItem(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    link = blocks.URLBlock()
    image = ImageBlock()

    class Meta:
        icon = 'item'


class SelectionGridPage(Page):
    body = StreamField([
        ('heading_hero', HeroImageBlock()),
        ('selection_grid', blocks.ListBlock(GridItem)),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    api_fields = (
        'body',
    )
