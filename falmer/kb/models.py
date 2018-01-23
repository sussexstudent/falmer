from graphql import GraphQLError
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import StreamBlock
from wagtail.wagtailcore.fields import StreamField

from falmer.content import components
from falmer.content.models.core import Page


class GuidePage(Page):
    pass


class ReferencePage(Page):
    main = StreamField(
        StreamBlock([
            components.text,
            components.callout,
            components.image,
            components.button_group_links,
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
    subpage_types = (ReferencePage, GuidePage, )

    def pages(self):
        return self.get_children().live()

    def section(self):
        return self.get_parent().specific

class SectionPage(Page):
    subpage_types = (TopicPage, )

    def topics(self):
        return self.get_children().live().specific()


class KnowledgeBaseRoot(Page):
    subpage_types = (SectionPage, )

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
