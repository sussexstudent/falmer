from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from falmer.content import components
from falmer.content.models.core import Page


class StubPage(Page):
    pass


class BasicContentPage(Page):
    content = StreamField(
        StreamBlock([
            components.text.to_pair(),
            components.callout.to_pair(),
            components.alert.to_pair(),
            components.inset.to_pair(),
            components.image.to_pair(),
            components.button_group_links.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    type_fields = ('content', )


