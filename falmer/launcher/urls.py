from django.conf.urls import url

from .views import launcher


urlpatterns = [
  url(r'^$', launcher),
]
