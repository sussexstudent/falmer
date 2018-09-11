import uuid
from collections import namedtuple

import requests
import bs4
import arrow
from django.db.models import Q
from django.utils import timezone
from fuzzywuzzy import process
from falmer.content.models.core import Page
from wagtail.search.backends import get_search_backend

from falmer.events.models import Event
from falmer.studentgroups.models import StudentGroup

MSLPageResult = namedtuple('MSLPageResult', ['uuid', 'link', 'title', 'description'])
MSLNewsResult = namedtuple('MSLNewsResult', ('uuid', 'link', 'title', 'description', 'image'))


def get_group_result(result):
    return {
        'uuid': str(uuid.uuid4()),
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': result.findNext('dd').text,
    }


def get_msl_page_result(result):
    return MSLPageResult(
        uuid=str(uuid.uuid4()),
        link=result.find('a')['href'].replace('..', ''),
        title=result.find('a').text,
        description=result.findNext('dd').text,
    )


def get_page_result(result):
    return {
        'uuid': str(uuid.uuid4()),
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': result.findNext('dd').text,
    }


def convert_page_result_to_object(page_dict):
    return MSLPageResult(
        uuid=page_dict['uuid'],
        link=page_dict['link'],
        title=page_dict['title'],
        description=page_dict['description'],
    )


def get_event_result(result):
    description = result.find(class_='event_description')
    location = result.find(class_='event_location')
    time = result.find(class_='event_time')

    return {
        'uuid': str(uuid.uuid4()),
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': description.text if description else None,
        'location': location.text if location else None,
        'time': time.text if time else None,
    }


def get_msl_news_result(result):
    anchor = result.select_one('h5 a')
    image = result.select_one('.news_image img')

    return MSLNewsResult(
        uuid=str(uuid.uuid4()),
        link=anchor['href'].replace('..', ''),
        title=anchor.text.replace('&nbsp;', ' '),
        description=result.find(class_='leader').text,
        image=image['src'] if image else None
    )


def get_news_result(result):
    anchor = result.select_one('h5 a')
    image = result.select_one('.news_image img')

    return {
        'uuid': str(uuid.uuid4()),
        'link': anchor['href'].replace('..', ''),
        'title': anchor.text.replace('&nbsp;', ' '),
        'description': result.find(class_='leader').text,
        'image': image['src'] if image else None,
    }


def get_results_for_term(term):

    s = get_search_backend()
    # get page
    req = requests.get('https://www.sussexstudent.com/msl-search/?q={}'.format(term))

    document = bs4.BeautifulSoup(req.text)

    groups = [get_group_result(result) for result in document.select('.search_groupings dt')]
    pages = [get_page_result(result) for result in document.select('.search_pages dt')]
    events = [get_event_result(result) for result in document.select('.search_events .event')]
    news = [get_news_result(result) for result in document.select('.search_news .news_item')]

    falmer_groups = s.search(term, StudentGroup.objects.all())
    falmer_events = s.search(term, Event.objects.all())

    all_unsorted = groups + pages + events + news
    results_map = {item['uuid']:item for item in all_unsorted}
    title_map = {item['title']:item['uuid'] for item in all_unsorted}

    fuzz_sorted = process.extract(term, title_map.keys(), limit=15)

    return {
        'results': results_map,
        'groups': [item['uuid'] for item in groups],
        'news': [item['uuid'] for item in news],
        'pages': [item['uuid'] for item in pages],
        'events': [item['uuid'] for item in events],
        'top': [title_map[fuzz_result[0]] for fuzz_result in fuzz_sorted],
    }


FalmerSearchQueryData = namedtuple('FalmerSearchQueryData', ('events', 'content', 'groups', ))
MSLSearchQueryData = namedtuple('MSLSearchQueryData', ('pages', 'news', ))

SearchTermResponseData = namedtuple('SearchQueryData', (
    'events',
    'content',
    'groups',
    'pages',
    'news',
    'top',
))


def get_msl_results_for_term(term):
    req = requests.get('https://www.sussexstudent.com/msl-search/?q={}'.format(term))

    document = bs4.BeautifulSoup(req.text)

    pages = [get_msl_page_result(result) for result in document.select('.search_pages dt')]
    news = [get_msl_news_result(result) for result in document.select('.search_news .news_item')]

    return MSLSearchQueryData(
        news=news,
        pages=pages
    )


def get_falmer_results_for_term(term):
    s = get_search_backend()

    falmer_content = Page.objects.live().search(term)
    falmer_events = s.search(term, Event.objects
                             .filter(
        Q(embargo_until=None) | Q(embargo_until__lte=timezone.now()),
        Q(mslevent__last_sync__gte=arrow.now().shift(minutes=-30).datetime) | Q(mslevent__isnull=True),
        start_time__gte=arrow.now().shift(hours=-24).datetime),
                             )
    falmer_groups = s.search(term, StudentGroup.objects.filter(Q(msl_group__last_sync__gte=arrow.now().shift(minutes=-90).datetime) | Q(msl_group__isnull=True)))

    return FalmerSearchQueryData(
        content=list(falmer_content),
        groups=list(falmer_groups),
        events=list(falmer_events),
    )

    # results_map = {item['uuid']:item for item in all_unsorted}
    # title_map = {item['title']:item['uuid'] for item in all_unsorted}
    #
    # fuzz_sorted = process.extract(term, title_map.keys(), limit=15)
    #
    # return {
    #     'results': results_map,
    #     'groups': [item['uuid'] for item in groups],
    #     'news': [item['uuid'] for item in news],
    #     'pages': [item['uuid'] for item in pages],
    #     'events': [item['uuid'] for item in events],
    #     'top': [title_map[fuzz_result[0]] for fuzz_result in fuzz_sorted],
    # }
    #
