from django.core.management import BaseCommand
from ...utils import sync_events_from_msl


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sync_events_from_msl()
