from django.http import JsonResponse
from .utils import get_results_for_term

def search(request):
    data = get_results_for_term(request.GET['q'])

    return JsonResponse({'results': data})
