from datetime import datetime
import re

import requests
import bs4

time_regex = re.compile(r"(([0-9]+):)?([0-9]+)(am|pm)|(midnight)")
date_regex = re.compile(r"([0-9]+)(?:rd|st|nd|th) (january|febuary|march|april|may|june|july|august|september|october|november|december)", flags=re.IGNORECASE)

MONTHS = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12,
}


def create_date(date, time):
    time = list(time[0])
    now = datetime.now()
    if time is None:
        return datetime(now.year, date['month'], date['day'])

    time_first = int(time[1]) if time[1] != '' else False
    time_second = int(time[2]) if time[2] != '' else False
    time_hour = time_first if time_first is not False else time_second
    time_minuets = 0 if time_first is False else time_second

    if time[4] == 'midnight':
        time[2] = '0'
        time[3] = 'am'

    additional = 12 if (time[3] == 'pm' and time_hour < 12) else 0

    return datetime(
        now.year,
        date['month'],
        date['day'],
        time_hour + additional,
        time_minuets
    )


def parse_date(date_string):
    time_match = [re.findall(time_regex, part) for part in date_string.split('-')]
    date_match = re.findall(date_regex, date_string)
    print(date_string)

    date_data = []

    for parsed_date in date_match:
        date_data.append({
            'month': MONTHS[parsed_date[1].lower()],
            'day': int(parsed_date[0]),
        })

    is_multi = len(date_data) > 1

    print(date_string)
    print(date_data)

    return {
        'start_date': create_date(date_data[0], time_match[0]),
        'end_date': create_date(
            date_data[1] if is_multi else date_data[0],
            time_match[1]
        ),
        'is_over_multiple_days': is_multi,
    }


def serialize_event(event):
    time = event.find(class_='msl_event_time').text
    org_name = event.find(class_='msl_event_organisation')
    dates = parse_date(time)

    return {
        'title': event.find(class_='msl_event_name').text,
        'organisationId': int(event['data-msl-organisation-id']),
        'organisationName': org_name.text if org_name else None,
        'link': event.find('a')['href'],
        'location': event.find(class_='msl_event_location').text,
        'time': time,
        'description': event.find(class_='msl_event_description').text,

        'startDate': dates['start_date'].isoformat(),
        'endDate': dates['end_date'].isoformat(),
        'isOverMultipleDays': dates['is_over_multiple_days'],
    }


def parse_events():
    # get page
    req = requests.get('https://www.sussexstudent.com/events/')

    document = bs4.BeautifulSoup(req.text)

    events = document.find_all(class_='event_item')

    return [serialize_event(event) for event in events]
