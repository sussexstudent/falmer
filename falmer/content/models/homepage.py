from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel


from falmer.content.blocks import FigureBlock
from falmer.content.models.core import Page


class HomePage(Page):
    parent_page_types = []

    full_time_officers = StreamField([
        ('figure', FigureBlock())
    ])
    part_time_officers = StreamField([
        ('figure', FigureBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('full_time_officers'),
        StreamFieldPanel('part_time_officers'),
    ]

    api_fields = (
        'full_time_officers',
        'part_time_officers',
    )

    type_fields = (
        'full_time_officers',
        'part_time_officers',
    )
