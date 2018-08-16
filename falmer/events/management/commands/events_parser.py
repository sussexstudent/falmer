import csv
import re

import markdown


# title = models.CharField(max_length=255)
# start_time = models.DateTimeField()
# end_time = models.DateTimeField()
#
# featured_image = models.ForeignKey(MatteImage, null=True, blank=False, on_delete=models.SET_NULL)
# url = models.URLField(blank=True, default='')
# social_facebook = models.URLField(blank=True, default='')
# kicker = models.CharField(max_length=255, default='')
# location_display = models.CharField(max_length=255, default='')
# embargo_until = models.DateTimeField(null=True)
#
# venue = models.ForeignKey(Venue, blank=True, null=True)
# short_description = models.TextField(default='')
#
# is_over_18_only = models.BooleanField(default=False)
# ticket_level = models.CharField(max_length=2, choices=TICKET_LEVEL_CHOICES, default=NA)
# cost = models.CharField(max_length=10, choices=COST_CHOICES, default=NA)
# alcohol = models.CharField(max_length=2, choices=ALCOHOL_CHOICES, default=NOT_ALCOHOL_FOCUSED)
#
# bundle = models.ForeignKey(Bundle, null=True, blank=True)
# category = models.ForeignKey(Category, null=True, blank=True)
# type = models.ForeignKey(Type, null=True, blank=True)
import datetime
import json


def parse_time(text):
    parts = text.split(':')
    mins = 0

    if len(parts) > 1:
        mins = int(parts[1])

    hour = int(parts[0])

    return hour, mins


def parse_bool(text):
    if text.lower() == 'yes':
        return True

    return False

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


available_columns = (
    'title',
    'body',
    'day',
    'start_time',
    'end_time',
    'short_description',

    'location',
    'type',
    'categories',

    'free',
    'is_over_18_only',

    'contains_loud_music',
    'contains_uneven_ground',
    'has_level_access',

    'audience_suitable_kids_families',
    'audience_just_for_pgs',
    'audience_good_to_meet_people',


    'alcohol_free',
    'alcohol_available',
)

START_ROW = 8
METADATA_ROW = 7


with open('f18.csv', 'r+', encoding='utf-8') as f:
    reader = csv.reader(f)
    parsed_events = []

    column_map = {}
    found_columns = []
    for index, row in enumerate(reader):
        def get_row(name):
            if name in found_columns:
                return row[column_map[name]]
            else:
                raise IndexError(f'{name} not found in map')
        if index == METADATA_ROW:
            for col_index, col in enumerate(row):
                if col in available_columns:
                    column_map[col] = col_index
                else:
                    print(col, 'not in av')
            found_columns = column_map.keys()
        elif index <= START_ROW:
            pass
        else:
            title = get_row('title')
            try:
                title = get_row('title')
                start_day = int(get_row('day').split(' ')[1].replace('th', '').replace('rd', '').replace('st', ''))

                start_time_hour, start_time_min = parse_time(get_row('start_time'))
                end_time_hour, end_time_min = parse_time(get_row('end_time'))
                alcohol_free_event = parse_bool(get_row('alcohol_free'))
                alcohol_available = parse_bool(get_row('alcohol_available'))
                free_event = parse_bool(get_row('free'))
                over_18_only = parse_bool(get_row('is_over_18_only'))
                parsed_events.append({
                    'title': title,
                    'start_time': datetime.datetime(2018, 9, start_day, start_time_hour, start_time_min),
                    'end_time': datetime.datetime(2018, 9, start_day if start_time_hour <= end_time_hour else start_day + 1, end_time_hour, end_time_min),
                    'short_description': get_row('short_description'),
                    'body': markdown.markdown(get_row('body')),
                    'location': get_row('location'),
                    'alcohol': 'NO' if alcohol_free_event and not alcohol_available else 'AV' if not alcohol_free_event and alcohol_available else 'NF',
                    'cost': 'FREE' if free_event else 'NA',
                    'is_over_18_only': over_18_only,
                    'type': get_row('type'),
                    'categories': [cat.strip() for cat in re.split(r'[:,;]', get_row('categories'))],
                    'audience_suitable_kids_families': parse_bool(get_row('audience_suitable_kids_families')),
                    'audience_just_for_pgs': parse_bool(get_row('audience_just_for_pgs')),
                    'audience_good_to_meet_people': parse_bool(get_row('audience_good_to_meet_people')),

                    'contains_loud_music': parse_bool(get_row('contains_loud_music')),
                    'contains_uneven_ground': parse_bool(get_row('contains_uneven_ground')),
                    'has_level_access': parse_bool(get_row('has_level_access')),

                })
            except (IndexError, ValueError) as e:
                print('failed to parse ', index, title, e)

    print(json.dumps({'events': parsed_events}, default=json_serial))
