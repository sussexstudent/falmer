from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, StreamFieldPanel, ObjectList

from falmer.content.blocks import HeroImageBlock, FalmerImageChooserBlock
from falmer.content.models.core import Page


class GridItem(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    link = blocks.URLBlock()
    image = FalmerImageChooserBlock()

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
