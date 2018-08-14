from django.db import models
from django.db.models import Q
from django.utils import timezone
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField

BANNER_PURPOSE_NOTICE = 'NOTICE'

BANNER_PURPOSE_CHOICES = (
    (BANNER_PURPOSE_NOTICE, 'Notice'),
)


class BannerManager(models.Manager):

    def all_active(self):
        return self.filter(
            Q(display_from__isnull=True) | Q(display_from__lte=timezone.now()),
            Q(display_to__isnull=True) | Q(display_to__gte=timezone.now()),
            disabled=False
        )


class Banner(models.Model):
    objects = BannerManager()

    outlet = models.CharField(max_length=64, blank=False, null=False)

    display_from = models.DateTimeField(blank=True, null=True)
    display_to = models.DateTimeField(blank=True, null=True)

    purpose = models.CharField(max_length=12, choices=BANNER_PURPOSE_CHOICES)

    heading = models.CharField(max_length=256, blank=True)
    body = RichTextField()

    disabled = models.BooleanField(default=False)

    panels = [
        FieldPanel('outlet'),
        FieldPanel('heading', classname='full title'),
        FieldPanel('body'),
        FieldPanel('display_from'),
        FieldPanel('display_to'),
        FieldPanel('purpose'),
        FieldPanel('disabled'),
    ]

    @property
    def is_active(self):
        return self.disabled is not True\
               and (self.display_from is None or self.display_from <= timezone.now())\
               and (self.display_to is None or self.display_to >= timezone.now())

    def __str__(self):
        return self.heading
