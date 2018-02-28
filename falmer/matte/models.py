import os
import uuid
from urllib.parse import urlparse
import boto3
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from .tasks import save_image_from_remote, perform_external_image_analysis

# image sources
# 100 - default, user wagtail
# 1xx - Reserved
# 2xx - Student Groups
# 3xx - Events
# 4xx - Book market

SOURCE_DEFAULT = 100

SOURCE_BOOK_MARKET_LISTING = 400

SOURCE_CHOICES = (
    (SOURCE_DEFAULT, 'Default'),
    (SOURCE_BOOK_MARKET_LISTING, 'Book Market - Listing'),
)


class MatteImage(AbstractImage):
    labels = models.ManyToManyField('matte.ImageLabel', through='matte.ImageLabelThrough')

    internal_source = models.IntegerField(choices=SOURCE_CHOICES, default=SOURCE_DEFAULT, null=False)

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

    def has_label_data(self):
        return self.external_metadata.last_label_request_time is not None

    def get_and_save_label_data(self):
        client = boto3.client(
            'rekognition',
            region_name='eu-west-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Name': self.file.name
                }
            },
            MaxLabels=60,
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            try:
                self.external_metadata
            except ImageExternalMetadata.DoesNotExist:
                self.external_metadata = ImageExternalMetadata()

            self.external_metadata.last_label_request_status = 'FAILED'
            self.external_metadata.save()
        else:
            self.labels.clear()
            labels = response['Labels']
            label_names = [label['Name'] for label in labels]

            found = ImageLabel.objects.filter(name__in=label_names)
            found_names = [label.name for label in found]
            missing = set(label_names) - set(found_names)

            created = ImageLabel.objects.bulk_create([ImageLabel(name=name) for name in missing])

            label_map = {}
            for label in created:
                label_map[label.name] = label
            for label in found:
                label_map[label.name] = label

            image_labels = []
            for label in labels:
                label_name = label['Name']
                if label_name in label_map:
                    image_labels.append(
                        ImageLabelThrough(
                            image=self,
                            label=label_map[label_name],
                            confidence=label['Confidence']
                        )
                    )

            ImageLabelThrough.objects.bulk_create(image_labels)

            try:
                self.external_metadata
            except ImageExternalMetadata.DoesNotExist:
                self.external_metadata = ImageExternalMetadata()

            self.external_metadata.last_label_request_time = timezone.now()
            self.external_metadata.last_label_request_status = 'OK'
            self.external_metadata.save()

        return response


class MatteRendition(AbstractRendition):
    image = models.ForeignKey(MatteImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(post_save, sender=MatteImage)
def image_create(sender, instance, created, **kwargs):
    if created:
        perform_external_image_analysis.delay(instance.pk)

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
    return parsed.scheme + '://' + parsed.netloc + parsed.path


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


class ImageExternalMetadata(models.Model):
    image = models.OneToOneField(
        MatteImage,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='external_metadata'
    )
    last_label_request_time = models.DateTimeField(null=True, blank=True)
    last_label_request_status = models.CharField(max_length=8, default='NA')


class ImageLabel(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class ImageLabelThrough(models.Model):
    label = models.ForeignKey(ImageLabel, on_delete=models.CASCADE)
    image = models.ForeignKey(MatteImage, on_delete=models.CASCADE)
    confidence = models.FloatField()

    class Meta:
        unique_together = (
            ('image', 'label'),
        )
