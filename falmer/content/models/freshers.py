from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField, RichTextField

from falmer.content.components.base import Component
from falmer.content.models.core import Page
from falmer.content import components

class TwoSlice(blocks.StructBlock):
    menu_name = blocks.CharBlock(required=True)
    background_color = blocks.CharBlock(required=True, max_length=7)

    title = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=True)

    col_one_title = blocks.CharBlock(required=True)
    col_one_content = StreamBlock([
        components.text.to_pair(),
        components.internal_link.to_pair(),
        components.external_link.to_pair(),
    ])

    col_two_title = blocks.CharBlock(required=True)
    col_two_content = StreamBlock([
        components.text.to_pair(),
        components.internal_link.to_pair(),
        components.external_link.to_pair(),
    ])


two_slice_component = Component('two_slice_component', TwoSlice)


class ProfileSlice(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=True)

    menu_name = blocks.CharBlock(required=True)
    background_color = blocks.CharBlock(required=True, max_length=7)

    body = StreamBlock([
        components.text.to_pair(),
        components.internal_link.to_pair(),
        components.external_link.to_pair(),
    ])

    image = components.image.block()


profile_slice_component = Component('profile_slice_component', ProfileSlice)


class FreshersHomepage(Page):
    countdown_caption = models.CharField(max_length=200)
    countdown_target = models.DateTimeField(blank=True, null=True)

    hero_text = RichTextField()

    content = StreamField(
        StreamBlock([
            two_slice_component.to_pair(),
            profile_slice_component.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero_text'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            FieldPanel('countdown_caption'),
            FieldPanel('countdown_target'),
        ], heading='Countdown'),
    ]
