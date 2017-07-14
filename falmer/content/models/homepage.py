from django.db import models
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, TabbedInterface, StreamFieldPanel, ObjectList
from wagtail.wagtailimages import get_image_model_string
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from falmer.content.blocks import FigureBlock


class HomePage(Page):
    full_time_officers = StreamField([
        ('figure', FigureBlock())
    ])
    part_time_officers = StreamField([
        ('figure', FigureBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('full_time_officers'),
        StreamFieldPanel('part_time_officers'),
    ]

    api_fields = (
        'full_time_officers',
        'part_time_officers',
    )
