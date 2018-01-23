import graphene
from graphene.types.generic import GenericScalar

from falmer.content import types as content_types


class KbGuide(content_types.Page):
    pass

class KbReference(content_types.Page):
    main = GenericScalar()
    topic = graphene.Field(lambda: KbTopic)

    def resolve_main(self, info):
        return self.main.stream_block.get_api_representation(self.main, info.context)

    def resolve_topic(self, info):
        return self.topic()


class KbArticle(content_types.Page):
    pass


class KbArticleTypes(graphene.Union):
    class Meta:
        types = (KbReference, KbGuide)


class KbTopic(content_types.Page):
    articles = graphene.List(KbArticle)
    section = graphene.Field(lambda: KbSection)

    def resolve_articles(self, info):
        return self.get_children().live()

    def resolve_section(self, info):
        return self.section()


class KbSection(content_types.Page):
    topics = graphene.List(KbTopic)

    def resolve_topics(self, info):
        return self.get_children().live().specific()


class KnowledgeBase(content_types.Page):
    sections = graphene.List(KbSection)
    section = graphene.Field(KbSection, slug=graphene.String())
    article = graphene.Field(KbReference, path=graphene.String())

    def resolve_sections(self, info):
        return self.sections()

    def resolve_section(self, info, **kwargs):
        return self.section_by_slug(kwargs.get('slug'))

    def resolve_article(self, info, **kwargs):
        return self.article_by_path(info.context, kwargs.get('path'))
