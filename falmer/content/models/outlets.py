from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from falmer.content import components
from falmer.content.components import structures
from falmer.events.models import Venue
from falmer.matte.models import MatteImage
from .core import Page


class OutletPage(Page):
    subpage_types = []
    parent_page_types = ('content.OutletIndexPage', )

    main = StreamField(
        StreamBlock([
            components.text.to_pair(),
        ]), verbose_name='Main Content',
        null=True, blank=True
    )

    hero_image = models.ForeignKey(MatteImage, null=False, blank=False, on_delete=models.PROTECT)

    opening_times = StreamField(StreamBlock([
        structures.opening_times.to_pair(),
    ]))

    menu = StreamField([
        components.document_link.to_pair()
    ], blank=True)

    deals = StreamField([
        components.text.to_pair(),
    ], blank=True)

    linked_venue = models.ForeignKey(Venue, blank=True, null=True, help_text='Link this outlet with a venue\'s events', on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        StreamFieldPanel('main'),
        ImageChooserPanel('hero_image'),
        StreamFieldPanel('opening_times'),
        StreamFieldPanel('menu'),
        StreamFieldPanel('deals'),
        FieldPanel('linked_venue'),
    ]

    api_fields = [
        'hero_image',
    ]


class OutletIndexPage(Page):
    subpage_types = (OutletPage, )

    preamble = StreamField([
        components.text.to_pair(),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('preamble'),
    ]

    api_fields = [
        'preamble',
    ]
