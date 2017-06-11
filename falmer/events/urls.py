from django.conf.urls import url

from .views import list_events

urlpatterns = [
  url(r'^$', list_events),
]
