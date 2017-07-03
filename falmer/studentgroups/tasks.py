from celery import shared_task
from .utils import sync_groups_from_msl


@shared_task
def sync_groups():
    sync_groups_from_msl()
