from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import DRFAuthenticatedGraphQLView

urlpatterns = [
    path('', csrf_exempt(DRFAuthenticatedGraphQLView.as_view(graphiql=True))),
]
