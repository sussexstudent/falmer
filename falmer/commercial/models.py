from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from falmer.content import components
from falmer.matte.models import MatteImage


class OfferCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Offer Category"
        verbose_name_plural = "Offer Categories"


class Offer(models.Model):
    company_name = models.CharField(
        max_length=255,
        blank=False,
        help_text='Display name of the company offering the deal'
    )

    company_logo = models.ForeignKey(
        MatteImage,
        blank=True,
        null=True,
        help_text='Companies logo displayed next to the offer',
        on_delete=models.SET_NULL
    )

    company_website = models.URLField(blank=True, default='')

    deal_tag = models.CharField(
        max_length=255,
        blank=False,
        help_text='The deal itself, "40%", "By one get one free", etc'
    )

    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(OfferCategory, blank=False, null=False, on_delete=models.CASCADE)

    main = StreamField(
        StreamBlock([
            components.text.to_pair(),
            components.image.to_pair(),
            components.callout.to_pair(),
        ], required=False),
        blank=True,
        help_text='Any additional information about this deal'
    )

    def __str__(self):
        return f'{self.deal_tag} @ {self.company_name}'

    panels = [
        FieldPanel('deal_tag', classname='full title'),
        FieldPanel('company_name', classname='full title'),
        FieldPanel('company_website'),
        FieldPanel('category'),
        FieldPanel('is_featured'),
        ImageChooserPanel('company_logo'),
        StreamFieldPanel('main'),
    ]
