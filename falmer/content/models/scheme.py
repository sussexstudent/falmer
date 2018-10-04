from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from falmer.content import components
from falmer.content.components.structures import sidebar_card
from falmer.content.models.mixins import SocialMediaMixin
from falmer.matte.models import MatteImage
from .core import Page


class SchemePage(Page, SocialMediaMixin):
    subpage_types = []
    parent_page_types = ('content.SchemeIndexPage', )

    main = StreamField(
        StreamBlock([
            components.text.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    hero_image = models.ForeignKey(MatteImage, null=False, blank=False, on_delete=models.PROTECT)

    sidebar_cards = StreamField([
        sidebar_card.to_pair()
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('main'),
        ImageChooserPanel('hero_image'),
        StreamFieldPanel('sidebar_cards'),
        MultiFieldPanel((
            FieldPanel('social_facebook_url'),
            FieldPanel('social_twitter_handle'),
            FieldPanel('social_snapchat_handle'),
            FieldPanel('social_instagram_handle'),
            FieldPanel('social_email_address'),
        )),
    ]

    api_fields = [
        'hero_image',
    ]


class SchemeIndexPage(Page):
    subpage_types = (SchemePage, )

    preamble = StreamField([
        components.text.to_pair(),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('preamble'),
    ]

    api_fields = [
        'preamble',
    ]
