from django.http import JsonResponse
from django.shortcuts import render

from falmer.events.serializers import EventSerializer
from .models import Event
from .utils import parse_events


def list_events(request):
    data = parse_events()

    link_keys = [item['link'] for item in data]

    event_matches = {event.msl_event_link: event for event in Event.objects.filter(msl_event_link__in=link_keys)}

    for item in data:
        model = event_matches.get(item['link'], None)

        item['falmer_event'] = None if model is None else EventSerializer(model).data

    return JsonResponse({'events': data})
