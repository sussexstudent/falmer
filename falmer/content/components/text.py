from wagtail.wagtailcore.blocks import StructBlock, RichTextBlock


class TextBlock(StructBlock):
    value = RichTextBlock()


text = ('text', TextBlock())
