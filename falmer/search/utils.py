import uuid
from collections import namedtuple

import requests
import bs4
from fuzzywuzzy import process
from falmer.content.models.core import Page
from wagtail.search.backends import get_search_backend

from falmer.events.models import Event
from falmer.studentgroups.models import StudentGroup

PageResult = namedtuple('PageResult', ['uuid', 'link', 'title', 'description'])


def get_group_result(result):
    return {
        'uuid': str(uuid.uuid4()),
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': result.findNext('dd').text,
    }


def get_page_result(result):
    return {
        'uuid': str(uuid.uuid4()),
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': result.findNext('dd').text,
    }


def convert_page_result_to_object(page_dict):
    return PageResult(
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

    print(falmer_groups)
    print(falmer_events)

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


def get_item_id(item):
    model = item.__class__.__name__
    return f'{model}_{item.pk}'


def get_item_title(item):
    if hasattr(item, 'title'):
        return item.title

    if hasattr(item, 'name'):
        return item.name

    return ''


SearchQueryData = namedtuple('SearchQueryData', ('events', 'content', 'groups', 'combined'))


def get_falmer_results_for_term(term):
    s = get_search_backend()

    falmer_content = Page.objects.search(term)
    falmer_groups = s.search(term, StudentGroup.objects.all())
    falmer_events = s.search(term, Event.objects.all())

    all_unsorted = list(falmer_content) + list(falmer_groups) + list(falmer_events)

    title_map = {get_item_title(item): get_item_id(item) for item in all_unsorted}

    fuzz_sorted = process.extract(term, title_map.keys(), limit=15)

    return SearchQueryData(
        content=falmer_content,
        groups=falmer_groups,
        events=falmer_events,
        combined=[title_map[fuzz_result[0]] for fuzz_result in fuzz_sorted],
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
