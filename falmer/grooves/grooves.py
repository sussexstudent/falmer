import requests
from django.conf import settings
from typing import TypeVar, Generic

T = TypeVar('T', bound='GroovesQuery')


def returnable(result):
    return result


class GroovesQuery(Generic[T]):
    def __init__(self, name: str, query: str, cache=-1, postprocess=returnable):
        self.name = name
        self.query = query
        self.cache = cache
        self.postprocess = postprocess

    def perform_query(self, variables: T):
        return requests.post(f'{settings.GROOVES_ENDPOINT}/query', json={
            'query': self.query,
            'variables': list(variables)
        }, headers={
            'x-query-token': settings.GROOVES_QUERY_TOKEN,
        })

    def get(self, variables: T):
        result = self.perform_query(variables)

        if result.ok:
            return self.postprocess(result.json()['result'])

        else:
            return False
