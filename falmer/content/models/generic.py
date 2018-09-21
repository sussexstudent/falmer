from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField, RichTextField

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

    related_links = StreamField(StreamBlock([('link_section', RelatedLinkSection())], required=False, blank=True), blank=True)
    staff_owners = StreamField(StreamBlock([('staff_member', StaffMemberChooser(StaffMemberSnippet))], required=False, blank=True), blank=True)

    promote_panels = [
        StreamFieldPanel('related_links'),
        StreamFieldPanel('staff_owners'),
    ]


class KBRootPage(Page):
    class Meta:
        verbose_name = 'Content Root'

    subpage_types = ('content.KBCategoryPage', )

    introduction = RichTextField(default='', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]


class KBCategoryPage(Page):
    parent_page_types = ('content.KBRootPage', )
    subpage_types = (
        'content.ReferencePage',
        'content.AnswerPage',
        'content.DetailedGuidePage',
    )

    page_icon = models.FileField(blank=True, null=True, default=None)

    content_panels = Page.content_panels + [
       FieldPanel('page_icon')
    ]

    @property
    def page_icon_url(self):
        return None if self.page_icon is None else self.page_icon.url


class ReferencePage(GenericContentPageMixin, Page):
    class Meta:
        verbose_name = 'Reference'

    parent_page_types = ('content.KBCategoryPage', )
    subpage_types = ()

    content = StreamField(
        StreamBlock([
            components.text.to_pair(),
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


class AnswerPage(GenericContentPageMixin, Page):
    class Meta:
        verbose_name = 'Answer'

    parent_page_types = ('content.KBCategoryPage', )
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


class DetailedGuidePage(GenericContentPageMixin, Page):
    class Meta:
        verbose_name = 'Detailed Guide'

    parent_page_types = ('content.KBCategoryPage', )
    subpage_types = ('content.DetailedGuideSectionPage', )

    promote_panels = Page.promote_panels + GenericContentPageMixin.promote_panels


class DetailedGuideSectionPage(Page):
    class Meta:
        verbose_name = 'Detailed Guide Section'

    parent_page_types = ('content.DetailedGuidePage', )

    content = StreamField(
        StreamBlock([
            components.text.to_pair(),
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

    def get_assumption_path(self):
        return self.get_parent().get_url_parts()[2][6:]
