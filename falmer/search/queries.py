import graphene

from falmer.search.types import SearchQuery
from falmer.search.utils import get_falmer_results_for_term


class Query(graphene.ObjectType):
    search = graphene.Field(SearchQuery, query=graphene.String())

    def resolve_search(self, info, query):
        results = get_falmer_results_for_term(query)

        print([type(result) for result in results])

        return results
