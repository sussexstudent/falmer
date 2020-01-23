import graphene
from fuzzywuzzy import process

from falmer.search.types import SearchQuery
from falmer.search.utils import get_falmer_results_for_term, get_msl_results_for_term, \
    SearchTermResponseData


def get_item_id(item):
    model = item.__class__.__name__ if hasattr(item, '__class__') else 'MSL'
    if model == 'Page':
        model = 'PageResult'
    id = item.pk if hasattr(item, 'pk') else item.uuid
    return f'{model}_{id}'


def get_item_title(item):
    if hasattr(item, 'title'):
        return item.title

    if hasattr(item, 'name'):
        return item.name

    return ''


class Query(graphene.ObjectType):
    search = graphene.Field(SearchQuery, query=graphene.String())

    def resolve_search(self, info, query):
        falmer_results = get_falmer_results_for_term(query)
        msl_results = get_msl_results_for_term(query)

        all_unsorted = falmer_results.content \
                       + falmer_results.groups \
                       + falmer_results.events \
                       + msl_results.pages \
                       + msl_results.news

        title_map = {}
        for item in all_unsorted:
            title_map[get_item_title(item)] = get_item_id(item)

        try:
            fuzz_sorted = process.extract(query, title_map.keys(), limit=15)
            top = [title_map[fuzz_result[0]] for fuzz_result in fuzz_sorted]
        except RuntimeError:
            top = []

        results = SearchTermResponseData(
            content=falmer_results.content,
            events=falmer_results.events,
            groups=falmer_results.groups,
            pages=msl_results.pages,
            news=msl_results.news,
            top=top,
        )

        return results
