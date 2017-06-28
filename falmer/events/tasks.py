from celery import Celery
from .utils import sync_events_from_msl


app = Celery()

@app.task
def sync_events():
    sync_events_from_msl()
