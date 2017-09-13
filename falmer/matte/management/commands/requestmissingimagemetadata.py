from django.core.management import BaseCommand
from ...models import MatteImage
from ...tasks import perform_external_image_analysis

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        images = MatteImage.objects.filter(external_metadata=None)

        for image in images:
            print('queuing {}'.format(image.pk))
            perform_external_image_analysis.delay(image.pk)
