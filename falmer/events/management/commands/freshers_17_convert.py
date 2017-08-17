import csv


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

with open('data.csv', 'r+', encoding='utf-8') as f:
    reader = csv.reader(f)
    parsed_events = []
    for index, row in enumerate(reader):
        if index <= 0:
            pass
        else:
            title = row[0]
            try:
                title = row[0]
                start_day = int(row[1].split(' ')[1])

                start_time_hour, start_time_min = parse_time(row[2])
                end_time_hour, end_time_min = parse_time(row[3])
                alcohol_free_event = parse_bool(row[10])
                alcohol_available = parse_bool(row[11])
                free_event = parse_bool(row[15])
                over_18_only = parse_bool(row[17])
                parsed_events.append({
                    'title': title,
                    'start_time': datetime.datetime(2017, 9, start_day, start_time_hour, start_time_min),
                    'end_time': datetime.datetime(2017, 9, start_day if start_time_hour <= end_time_hour else start_day + 1, end_time_hour, end_time_min),
                    'short_desc': row[4],
                    'long_desc': row[5],
                    'venue_name': row[8],
                    'alcohol': 'NO' if alcohol_free_event and not alcohol_available else 'AV' if not alcohol_free_event and alcohol_available else 'NF',
                    'cost': 'FREE' if free_event else 'NA' if row[7].lower() == 'n/a' else 'PAID',
                    'is_over_18_only': over_18_only,
                    'suitable_kids_families': parse_bool(row[20]),
                    'just_for_pgs': parse_bool(row[25]),
                })
            except (IndexError, ValueError):
                print('failed to parse ', index, title)

    print(json.dumps({'events': parsed_events}, default=json_serial))
