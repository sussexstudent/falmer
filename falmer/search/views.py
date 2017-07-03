from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .utils import get_results_for_term


@api_view(['GET'])
@permission_classes([AllowAny, ])
def search(request):
    search_term = request.GET['q']
    cache_key = 'sr_{}'.format(search_term)

    cached = cache.get(cache_key)

    if cached is not None:
        return Response(cached)

    data = get_results_for_term(search_term)

    cache.set(cache_key, data, 60 * 60)

    return Response(data)
