from django.conf.urls import url

from .views import ListMembersAPIView

urlpatterns = [
  url(r'^(?P<list_slug>[-\w]+)/members$', ListMembersAPIView.as_view()),
]
