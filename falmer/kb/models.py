from graphql import GraphQLError
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField

from falmer.content import components
from falmer.content.models.core import Page


class GuidePage(Page):
    parent_page_types = ('kb.TopicPage', )


class KBReferencePage(Page):
    parent_page_types = ('kb.TopicPage', )

    main = StreamField(
        StreamBlock([
            components.text.to_pair(),
            components.callout.to_pair(),
            components.image.to_pair(),
            components.button_group_links.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('main'),
    ]

    def topic(self):
        return self.get_parent().specific


class TopicPage(Page):
    subpage_types = (KBReferencePage, GuidePage, )
    parent_page_types = ('kb.SectionPage', )

    def pages(self):
        return self.get_children().live()

    def section(self):
        return self.get_parent().specific


class SectionPage(Page):
    subpage_types = (TopicPage, )
    parent_page_types = ('kb.KnowledgeBaseRoot', )

    def topics(self):
        return self.get_children().live().specific()


class KnowledgeBaseRoot(Page):
    subpage_types = (SectionPage, )
    parent_page_types = []

    def sections(self):
        return self.get_children().live().specific()

    def section_by_slug(self, slug):
        try:
            return self.get_live_children().specific().get(slug=slug)
        except Page.DoesNotExist:
            raise GraphQLError('Does not exist')

    def article_by_path(self, request, path):
        result = self.route(request, path.split('/'))
        return result.page
