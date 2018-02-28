from wagtail.wagtailcore.blocks import StructBlock, RichTextBlock

from falmer.content.components.base import Component


class TextBlock(StructBlock):
    value = RichTextBlock()


text = Component('text', TextBlock)
