import uuid
import requests
import bs4
from fuzzywuzzy import process

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
        'title': anchor.text,
        'description': result.find(class_='leader').text,
        'image': image['src'] if image else None,
    }


def get_results_for_term(term):
    # get page
    req = requests.get('https://www.sussexstudent.com/search/?q={}'.format(term))

    document = bs4.BeautifulSoup(req.text)

    groups = [get_group_result(result) for result in document.select('.search_groupings dt')]
    pages = [get_page_result(result) for result in document.select('.search_pages dt')]
    events = [get_event_result(result) for result in document.select('.search_events .event')]
    news = [get_news_result(result) for result in document.select('.search_news .news_item')]


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
