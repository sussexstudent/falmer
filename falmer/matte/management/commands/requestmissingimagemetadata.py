from django.core.management import BaseCommand
from ...models import MatteImage


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        image = MatteImage.objects.get(pk=127)
        print(image.get_and_save_label_data())
