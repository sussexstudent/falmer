from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import open_falmer


urlpatterns = [
  path('open-falmer/', csrf_exempt(open_falmer)),
]
