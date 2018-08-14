from django.db import models
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, StreamFieldPanel, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel

from falmer.content.blocks import PledgeBlock
from falmer.content.models.core import Page
from falmer.matte.models import MatteImage


class OfficersIndex(Page):
    pass


class OfficerOverviewPage(Page):
    role = models.CharField(max_length=255)
    role_description = RichTextField()

    officer_image = models.ForeignKey(MatteImage, null=True, blank=False, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    manifesto_tagline = models.CharField(max_length=255)
    manifesto_overview = RichTextField()

    twitter_username = models.CharField(max_length=30)

    pledges = StreamField([
        ('pledge', PledgeBlock()),
    ])

    parent_page_types = ('content.OfficersIndex', )

    content_panels = Page.content_panels + [
        FieldPanel('role'),
        FieldPanel('role_description'),
        ImageChooserPanel('officer_image'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('manifesto_tagline'),
        FieldPanel('manifesto_overview'),
        FieldPanel('twitter_username'),
        StreamFieldPanel('pledges'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    api_fields = (
        'role',
        'role_description',
        'officer_image',
        'first_name',
        'last_name',
        'manifesto_tagline',
        'manifesto_overview',
        'twitter_username',
        'pledges',
    )
