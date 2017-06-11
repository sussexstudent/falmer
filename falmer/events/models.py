from django.db import models

from falmer.matte.models import MatteImage

SL_ROOM_76 = 'ROOM_76'
SL_FALMER_BAR = 'FALMER_BAR'
SL_EAST_SLOPE = 'EAST_SLOPE'

SL_CHOICES = (
    (SL_ROOM_76, 'Room 76'),
    (SL_FALMER_BAR, 'Falmer Bar'),
    (SL_EAST_SLOPE, 'East Slope'),
)


class Event(models.Model):
    msl_event_link = models.CharField(max_length=255, unique=True, blank=False, null=False)

    featured_image = models.ForeignKey(MatteImage, null=True, blank=False, on_delete=models.SET_NULL)
    social_facebook = models.URLField(blank=True, default='')
    smart_location = models.CharField(max_length=20, choices=SL_CHOICES, blank=True, null=True)
