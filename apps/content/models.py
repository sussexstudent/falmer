from django.db import models
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages import get_image_model_string
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class StaffPage(Page):
    subpage_types = ('StaffDepartment',)


class StaffDepartment(Page):
    subpage_types = ('StaffSection',)


class StaffSection(Page):
    content_panels = Page.content_panels + [
        InlinePanel('staff', label="Staff"),
    ]


class StaffMember(Orderable):
    department = ParentalKey(StaffSection, related_name='staff')
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    office_phone_number = models.CharField(max_length=255, null=True, blank=True)
    mobile_phone_number = models.CharField(max_length=255, null=True, blank=True)
    job_description = RichTextField()
    office_location = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('job_title'),
        FieldPanel('email'),
        FieldPanel('office_phone_number'),
        FieldPanel('mobile_phone_number'),
        ImageChooserPanel('photo'),
        FieldPanel('job_description'),
    ]
