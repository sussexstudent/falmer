from wagtail.core.blocks import StructBlock

from falmer.content.blocks import RichTextWithExpandedContent
from falmer.content.components.base import Component


class TextBlock(StructBlock):
    value = RichTextWithExpandedContent(features=['h2', 'bold', 'italic', 'ol', 'ul', 'hr', 'link'])


text = Component('text', TextBlock)
