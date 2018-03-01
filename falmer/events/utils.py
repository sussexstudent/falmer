import arrow
import requests
from .models import MSLEvent


def get_msl_events_from_api(month_multiplier=1):

    # at the moment, msl only allows 3 month max event range
    from_date = arrow.utcnow()
    if month_multiplier > 1:
        from_date = from_date.shift(months=3 * (month_multiplier - 1))

    req = requests.get('https://www.sussexstudent.com/svc/feeds/events/0?subtree=true&from={from_date}&imagesize=event'.format(
        from_date=from_date.format('YYYY-MM-DD')
    ))

    if req.status_code == 200:
        return req.json()

    return []


def sync_events_from_msl():
    msl_events_requests = [get_msl_events_from_api(m) for m in range(0, 5)]

    msl_events = [y for x in msl_events_requests for y in x]
    msl_events_map = {item['Id']: item for item in msl_events}
    msl_event_ids = set(msl_events_map)
    event_matches = {event.msl_event_id: event for event in MSLEvent.objects.filter(msl_event_id__in=msl_event_ids)}

    report = {}

    for msl_event_id in msl_event_ids:
        if msl_event_id in event_matches:
            event_matches[msl_event_id].update_from_msl(msl_events_map[msl_event_id])
            report[msl_event_id] = 'updated'
        else:
            # MSLEvent.create_from_msl(msl_events_map[msl_event_id])
            report[msl_event_id] = 'created new'

    print(report)
