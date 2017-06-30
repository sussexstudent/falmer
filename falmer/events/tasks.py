from celery import shared_task
from .utils import sync_events_from_msl


@shared_task
def sync_events():
    sync_events_from_msl()
