import json

import datetime
import arrow
import requests
from dateutil import tz
from django.core.management import BaseCommand

from falmer.events.models import Event, BrandingPeriod, Type, CategoryNode


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_uri', type=str)

    def handle(self, *args, **kwargs):
        res = requests.get(kwargs['file_uri'])

        data = res.json()

        events_list = data['events']

        freshers, created = BrandingPeriod.objects.get_or_create(
            name='Freshers Week 2018',
            slug='freshers-week-2018',
        )

        print('{} events to be added.'.format(len(events_list)))

        start = input('Is this correct? y/n?')

        if start != 'y':
            return

        for event in events_list:
            print(event['title'])
            print(event['type'])
            t, c = Type.objects.get_or_create(name__iexact=event['type'])
            print(t, c)
            event_instance = Event(
                title=event['title'],
                start_time=arrow.get(event['start_time']).replace(tzinfo=tz.gettz('Europe/London')).datetime,
                end_time=arrow.get(event['end_time']).replace(tzinfo=tz.gettz('Europe/London')).datetime,
                location_display=event['location'],
                short_description=event['short_description'],
                body=event['body'],
                is_over_18_only=event['is_over_18_only'],
                alcohol=event['alcohol'],
                cost=event['cost'],
                audience_suitable_kids_families=event['audience_suitable_kids_families'],
                audience_just_for_pgs=event['audience_just_for_pgs'],
                audience_good_to_meet_people=event['audience_good_to_meet_people'],
                contains_loud_music=event['contains_loud_music'],
                contains_uneven_ground=event['contains_uneven_ground'],
                has_level_access=event['has_level_access'],
                type=t,
                brand=freshers,
                embargo_until=datetime.datetime(2018, 9, 20, 12, 0).replace(tzinfo=tz.gettz('Europe/London')),
            )

            event_instance.save()

            for cat in event['categories']:
                try:
                    event_instance.category.add(CategoryNode.objects.get(name__iexact=cat))
                except CategoryNode.DoesNotExist:
                    print(f'missing category: {cat}')
