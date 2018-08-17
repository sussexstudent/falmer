import json
import datetime
import arrow
import requests
from dateutil import tz
from django.core.management import BaseCommand
from django.db import IntegrityError

from falmer.events.models import Event, BrandingPeriod, Type, CategoryNode

pa_fix_columns = (
    'contains_loud_music',
    'contains_uneven_ground',
    'has_level_access',
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        try:
            freshers = BrandingPeriod.objects.get(
                slug='freshers-week-2018',
            )
        except BrandingPeriod.DoesNotExist:
            raise ValueError('freshers week period does not exist')

        events = Event.objects.filter(brand=freshers)

        print(f'This will fix {len(events)}')

        con = input('Continue? y/n')

        if con != 'y':
            exit(0)

        for event in events:
            try:
                # change embargo to August - oppsie!
                event.embargo_until = datetime.datetime(2018, 8, 20, 12, 0).replace(tzinfo=tz.gettz('Europe/London'))

                # fix true/false pa value bug
                # 0=na, 1=false, 2=true; we imported as true/false. thus false=na, true=false.
                event.contains_loud_music = event.contains_loud_music + 1
                event.contains_uneven_ground = event.contains_uneven_ground + 1
                event.has_level_access = event.has_level_access + 1

                event.save()
            except IntegrityError:
                print(f'-> failed to save: {event.title}')

        print('complete!')
