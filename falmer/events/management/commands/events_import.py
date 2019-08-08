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
            name='Freshers Week',
            slug='freshers-week-2019',
        )

        print('{} events to be added.'.format(len(events_list)))

        start = input('Is this correct? y/n?')

        if start != 'y':
            return

        for event in events_list:
            print(event['title'])
            if event['type'] != '':
                event_type = event['type']
                try:
                    t = Type.objects.get(name__iexact=event_type)
                except Type.DoesNotExist:
                    print(f'creating type "{event_type}"')
                    t = Type.objects.create(name=event_type)
            else:
                t = None
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
                embargo_until=datetime.datetime(2019, 9, 15, 0, 0).replace(tzinfo=tz.gettz('Europe/London')),
            )

            event_instance.save()

            for cat in event['categories']:
                cat_instance = CategoryNode.objects.filter(name__iexact=cat.replace('and', '&')).first()
                if cat_instance is not None:
                    event_instance.category.add(cat_instance)
                else:
                    print(f'-> missing category: {cat}')
