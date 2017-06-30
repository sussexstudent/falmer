import logging
import os
import tempfile

import requests
from io import BytesIO
from celery import Celery
from django.core import files

from .utils import create_image_from_bytes

logger = logging.getLogger(__name__)

app = Celery()

@app.task
def save_image_from_remote(remote_image_pk):
    from .models import RemoteImage
    try:
        remote = RemoteImage.objects.get(pk=remote_image_pk)
        request = requests.get(remote.image_url, stream=True)
        if request.status_code != requests.codes.ok:
            return
        file_name = remote.image_url.split('/')[-1]

        lf = tempfile.NamedTemporaryFile()

        # Read the streamed image in sections
        for block in request.iter_content(1024 * 8):

            # If no more file then stop
            if not block:
                break

            # Write image block to temporary file
            lf.write(block)

        image_model = create_image_from_bytes(files.File(lf), file_name)

        if image_model is not None:
            remote.matte_image = image_model
            remote.save()

    except RemoteImage.DoesNotExist:
        logger.error('Tried to load a remote image model that did not exist', exc_info=True)

