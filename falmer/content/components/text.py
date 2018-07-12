from wagtail.core.blocks import StructBlock, RichTextBlock

from falmer.content.components.base import Component


class TextBlock(StructBlock):
    value = RichTextBlock(features=['h2', 'bold', 'italic', 'ol', 'ul', 'hr'])


text = Component('text', TextBlock)
