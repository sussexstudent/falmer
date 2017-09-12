import os
import uuid
from urllib.parse import urlparse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from .tasks import save_image_from_remote

class MatteImage(AbstractImage):

    admin_form_fields = Image.admin_form_fields + (
        # nothing yet
    )

    class Meta:
        permissions = (
            ('can_list_all', 'Can list all images'),
        )

    def get_upload_to(self, filename):
        folder_name = 'original_images'

        return os.path.join(folder_name, str(uuid.uuid4()).replace('-', ''))


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


def normalize_url(url):
    parsed = urlparse(url)
    return parsed.scheme + "://" + parsed.netloc + parsed.path


class RemoteImage(models.Model):
    image_url = models.URLField(unique=True)
    matte_image = models.ForeignKey(MatteImage, null=True)

    def __str__(self):
        return self.image_url

    @staticmethod
    def try_image(url):
        if url is None or url == '':
            return None

        url = normalize_url(url)

        try:
            record = RemoteImage.objects.get(image_url=url)

            if record.matte_image is not None:
                return record.matte_image
            else:
                return None
        except RemoteImage.DoesNotExist:
            record = RemoteImage.objects.create(
                image_url=url,
                matte_image=None,
            )

            save_image_from_remote.delay(record.pk)

            return None


    # any msl image:
        # MSLImage?
            # has matte?
                # return matte
            # if not do nothing
        # else
            # create empty msl image
            # add task to queue
