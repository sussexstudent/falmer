from wagtail.wagtailcore.blocks import StructBlock, RichTextBlock, ChoiceBlock
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


callout = ('callout', CalloutBlock())

