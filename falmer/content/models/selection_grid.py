from wagtail.core import blocks
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import TabbedInterface, StreamFieldPanel, ObjectList

from falmer.content import components
from falmer.content.blocks import HeroImageBlock, FalmerImageChooserBlock
from falmer.content.models.core import Page


class GridItem(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    link = blocks.URLBlock()
    image = FalmerImageChooserBlock()
    description = RichTextBlock(required=False)

    class Meta:
        icon = 'item'


class SelectionGridPage(Page):
    body = StreamField([
        ('heading_hero', HeroImageBlock()),
        components.text.to_pair(),
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

    type_fields = (
        'body',
    )
