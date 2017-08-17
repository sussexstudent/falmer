import json

import datetime
import arrow
from dateutil import tz
from django.core.management import BaseCommand

from falmer.events.models import Event, BrandingPeriod
from ...utils import sync_events_from_msl


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['file_path'], 'r+') as file:
            data = json.load(file)

            events_list = data['events']

            freshers = BrandingPeriod(
                name='Freshers Week 2017',
            )

            freshers.save()

            print('{} events to be added.'.format(len(events_list)))

            for event in events_list:
                print(event['title'])
                event_instance = Event(
                    title=event['title'],
                    start_time=arrow.get(event['start_time']).replace(tzinfo=tz.gettz('Europe/London')).datetime,
                    end_time=arrow.get(event['end_time']).replace(tzinfo=tz.gettz('Europe/London')).datetime,
                    location_display=event['venue_name'],
                    short_description=event['short_desc'],
                    body=event['long_desc'],
                    is_over_18_only=event['is_over_18_only'],
                    alcohol=event['alcohol'],
                    cost=event['cost'],
                    suitable_kids_families=event['suitable_kids_families'],
                    just_for_pgs=event['just_for_pgs'],
                    brand=freshers,

                    embargo_until=datetime.datetime(2017, 8, 21, 12, 0),
                )

                event_instance.save()
