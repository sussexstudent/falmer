from wagtail.core.blocks import StructBlock, RichTextBlock, ChoiceBlock, TextBlock

from falmer.content.components.base import Component


class CalloutBlock(StructBlock):
    value = TextBlock()

    variant = ChoiceBlock(
        label='Variant',
        choices=(
            ('info', 'Info'),
            ('alert', 'Alert'),
        )
    )


callout = Component('callout', CalloutBlock)


class AlertBlock(StructBlock):
    value = RichTextBlock(features=['italic', ])


alert = Component('alert_text', AlertBlock)


class InsetBlock(StructBlock):
    value = RichTextBlock(features=['italic', ])


inset = Component('inset_text', AlertBlock)

