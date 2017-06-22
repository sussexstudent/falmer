from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from falmer.content.serializers import WagtailImageSerializer


class ImageBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        return WagtailImageSerializer(value).data


class ContactBlock(blocks.StructBlock):
    body = blocks.TextBlock()
    name = blocks.CharBlock()
    email = blocks.EmailBlock()

    class Meta:
        icon = 'user'


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    body = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
    ])

    class Meta:
        icon = 'user'


class PledgeBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    body = blocks.RichTextBlock(required=True)
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
