from wagtail.core.blocks import StructBlock, RichTextBlock, ChoiceBlock

from falmer.content.components.base import Component
from .text import TextBlock


class CalloutBlock(StructBlock):
    value = TextBlock()
    variant = ChoiceBlock(
        label='Variant',
        choices=(
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('alert', 'Alert'),
        )
    )


callout = Component('callout', CalloutBlock)

