from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from falmer.content import components
from falmer.content.components.links import ButtonGroupLinks
from falmer.content.models.core import Page
from falmer.content.models.staff import StaffMemberChooser, StaffMemberSnippet


class RelatedLinkSection(blocks.StructBlock):
    name = blocks.CharBlock(required=False)
    links = ButtonGroupLinks()


class GenericContentPageMixin(models.Model):
    class Meta:
        abstract = True

    related_links = StreamField([('link_section', RelatedLinkSection())])
    staff_owners = StreamField([('staff_member', StaffMemberChooser(StaffMemberSnippet))])

    promote_panels = [
        StreamFieldPanel('related_links'),
        StreamFieldPanel('staff_owners'),
    ]


    api_fields = [
        'related_links',
        'staff_owners',
    ]

class ContentRootPage(Page):
    class Meta:
        verbose_name = 'Content Root'

    subpage_types = (
        'content.ReferencePage',
        'content.AnswerPage',
        'content.DetailedGuidePage',
    )


class ReferencePage(GenericContentPageMixin, Page):
    class Meta:
        verbose_name = 'Reference'

    parent_page_types = ('content.ContentRootPage', )
    subpage_types = ()

    content = StreamField(
        StreamBlock([
            components.text.to_pair(),
            components.callout.to_pair(),
            components.alert.to_pair(),
            components.inset.to_pair(),
            components.image.to_pair(),
            components.button_group_links.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    promote_panels = Page.promote_panels + GenericContentPageMixin.promote_panels

    api_fields = GenericContentPageMixin.api_fields + [
        'content',
    ]


class AnswerPage(GenericContentPageMixin, Page):
    class Meta:
        verbose_name = 'Answer'

    parent_page_types = ('content.ContentRootPage', )
    subpage_types = ()

    content = StreamField(
        StreamBlock([
            components.text.to_pair(),
            components.alert.to_pair(),
            components.inset.to_pair(),
            components.image.to_pair(),
            components.button_group_links.to_pair(),
            components.start_button.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    promote_panels = Page.promote_panels + GenericContentPageMixin.promote_panels

    api_fields = GenericContentPageMixin.api_fields + [
        'content',
    ]


class DetailedGuidePage(GenericContentPageMixin, Page):
    class Meta:
        verbose_name = 'Detailed Guide'

    parent_page_types = ('content.ContentRootPage', )
    subpage_types = ('content.DetailedGuideSectionPage', )

    promote_panels = Page.promote_panels + GenericContentPageMixin.promote_panels


class DetailedGuideSectionPage(Page):
    class Meta:
        verbose_name = 'Detailed Guide Section'

    parent_page_types = ('content.DetailedGuidePage', )

    content = StreamField(
        StreamBlock([
            components.text.to_pair(),
            components.callout.to_pair(),
            components.alert.to_pair(),
            components.inset.to_pair(),
            components.image.to_pair(),
            components.button_group_links.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    promote_panels = Page.promote_panels

    api_fields = [
        'content',
    ]

    def get_assumption_path(self):
        return self.get_parent().get_url_parts()[2][6:]
