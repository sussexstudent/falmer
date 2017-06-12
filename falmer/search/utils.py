from datetime import datetime
import re

import requests
import bs4

def get_group_result(result):

    return {
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': result.findNext('dd').text,
    }

def get_page_result(result):

    return {
        'link': result.find('a')['href'].replace('..', ''),
        'title': result.find('a').text,
        'description': result.findNext('dd').text,
    }


def get_event_result(result):
    description = result.find(class_='event_description')
    location = result.find(class_='event_location')
    time = result.find(class_='event_time')

    return {
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
        'link': anchor['href'].replace('..', ''),
        'title': anchor.text,
        'description': result.find(class_='leader').text,
        'image': image['src'] if image else None,
    }


def get_results_for_term(term):
    # get page
    req = requests.get('https://www.sussexstudent.com/search/?q={}'.format(term))

    document = bs4.BeautifulSoup(req.text)

    groups = [get_group_result(result) for result in document.select('.search_groupings dt')[:10]]
    pages = [get_page_result(result) for result in document.select('.search_pages dt')[:10]]
    events = [get_event_result(result) for result in document.select('.search_events .event')[:10]]
    news = [get_news_result(result) for result in document.select('.search_news .news_item')[:10]]

    return {
        'groups': groups,
        'news': news,
        'pages': pages,
        'events': events,
    }
