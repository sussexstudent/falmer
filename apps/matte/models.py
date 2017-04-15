from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition


class MatteImage(AbstractImage):

    admin_form_fields = Image.admin_form_fields + (
        # nothing yet
    )


class MatteRendition(AbstractRendition):
    image = models.ForeignKey(MatteImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(post_delete, sender=MatteImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(post_delete, sender=MatteRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
