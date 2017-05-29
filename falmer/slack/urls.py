from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import open_falmer


urlpatterns = [
  url(r'^open-falmer/', csrf_exempt(open_falmer)),
]
