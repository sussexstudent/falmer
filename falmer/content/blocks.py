from wagtail.core import blocks
from wagtail.core.blocks import RichTextBlock, PageChooserBlock
from wagtail.core.rich_text import expand_db_html
from wagtail.images.blocks import ImageChooserBlock

from falmer.content.serializers import WagtailImageSerializer
from falmer.content.utils import get_public_path_for_page


class FalmerPageChooserBlock(PageChooserBlock):
    def get_api_representation(self, value, context=None):

        if value is None:
            return None

        return {
            'title': value.title,
            'path': get_public_path_for_page(value),
        }


class FalmerImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        return WagtailImageSerializer(value).data


ImageBlock = FalmerImageChooserBlock


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
    heading_image = FalmerImageChooserBlock(required=False)
    body = blocks.StreamBlock([
        ('paragraph', RichTextWithExpandedContent()),
    ])

    class Meta:
        icon = 'user'


class FigureBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=True)
    image = FalmerImageChooserBlock()
    link = blocks.CharBlock(required=False)

    class Meta:
        icon = 'user'


class PledgeBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    body = RichTextWithExpandedContent(required=True)
    image = FalmerImageChooserBlock()
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
    image = FalmerImageChooserBlock()

    class Meta:
        icon = 'image'
