from wagtail.core import blocks
from django.utils.translation import ugettext_lazy as _
from wagtail.documents.blocks import DocumentChooserBlock

from falmer.content.blocks import FalmerPageChooserBlock
from falmer.content.components.base import Component
from falmer.content.serializers import DocumentLinkSerializer

TARGETS = (
    ('', 'Open link in'),
    ('_self', 'Same window'),
    ('_blank', 'New window'),
)


class InternalLink(blocks.StructBlock):
    """
    Single Internal link block
    """
    link = FalmerPageChooserBlock(required=True)
    title = blocks.CharBlock(required=False)

    @property
    def get_title(self):
        if self.title:
            return self.title
        else:
            self.link.title

    class Meta:
        icon = 'link'


internal_link = Component('internal_link', InternalLink)


class DocumentLink(blocks.StructBlock):
    """
    Single Internal link block
    """
    link = DocumentChooserBlock(required=True)
    title = blocks.CharBlock(required=False)

    @property
    def get_title(self): # weird; property with get_
        if self.title:
            return self.title
        else:
            self.link.name

    class Meta:
        icon = 'link'

    def get_api_representation(self, value, context=None):
        return DocumentLinkSerializer(value).data


document_link = Component('document_link', DocumentLink)


class ExternalLink(blocks.StructBlock):
    """
    Single External Tile Block
    """
    link = blocks.URLBlock(required=True)
    title = blocks.CharBlock(required=True)
    target = blocks.ChoiceBlock(
        required=True,
        choices=TARGETS,
        default='_self',
        help_text=_('Open link in')
    )

    class Meta:
        icon = 'site'


external_link = Component('external_link', ExternalLink)


class ButtonGroupLinks(blocks.StreamBlock):
    """
    A collection of Link Blocks, Orderable
    """
    internal_link = InternalLink(label=_('Internal page'))
    external_link = ExternalLink(label=_('External Page'))

    class Meta:
        icon = 'link'


button_group_links = Component('button_group_links', ButtonGroupLinks)
