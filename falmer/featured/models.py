import arrow
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q

from falmer.core.models import TimeStampedModel
from falmer.matte.models import MatteImage


class SlateManager(models.Manager):
    def active(self):
        try:
            return self.get(
                Q(display_from__lte=arrow.utcnow().datetime) | Q(display_from__isnull=True))
        except Slate.DoesNotExist:
            return None


class Slate(TimeStampedModel, models.Model):
    objects = SlateManager()

    display_from = models.DateTimeField()
    data = JSONField()
    notes = models.TextField(default='')

    def enhanced_data(self):
        final = self.data
        for area in self.data['areas']:
            for box in area:
                for key in box['data'].keys():
                    if key.endswith('Image'):
                        img = MatteImage.objects.get(pk=box['data'][key])
                        box['data'][key] = {'resource': img.file.name, 'width': img.width,
                                            'height': img.height}

        return final
