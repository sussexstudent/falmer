from django.core.management import BaseCommand
from ...models import RemoteImage
from ...tasks import save_image_from_remote


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        images = RemoteImage.objects.filter(matte_image=None)

        for image in images:
            save_image_from_remote.delay(image.pk)
