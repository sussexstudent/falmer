from django.urls import path

from .views import list_events

urlpatterns = [
  path('', list_events),
]
