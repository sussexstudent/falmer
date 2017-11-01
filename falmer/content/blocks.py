from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import RichTextBlock
from wagtail.wagtailcore.rich_text import expand_db_html
from wagtail.wagtailimages.blocks import ImageChooserBlock

from falmer.content.serializers import WagtailImageSerializer


class ImageBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        return WagtailImageSerializer(value).data


class RichTextWithExpandedContent(RichTextBlock):
    def get_prep_value(self, value):
        return expand_db_html(value.source)


class ContactBlock(blocks.StructBlock):
    body = blocks.TextBlock()
    name = blocks.CharBlock()
    email = blocks.EmailBlock()

    class Meta:
        icon = 'user'


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', RichTextWithExpandedContent()),
    ])

    class Meta:
        icon = 'user'


class FigureBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=True)
    image = ImageBlock()
    link = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'


class PledgeBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    body = RichTextWithExpandedContent(required=True)
    image = ImageBlock()
    status = blocks.ChoiceBlock(choices=[
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('blank', 'Blank'),
        ]
    )

    class Meta:
        icon = 'text'


class HeroImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text='Leave empty to use the page title')
    image = ImageBlock()

    class Meta:
        icon = 'image'
