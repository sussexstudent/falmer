from django.core.management import BaseCommand
from ...models import MatteImage
from ...tasks import perform_external_image_analysis

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        images = MatteImage.objects.filter(external_metadata__last_label_request_status='NA')

        for image in images:
            perform_external_image_analysis.delay(image.pk)
