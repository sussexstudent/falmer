from django.conf.urls import url

from .views import Image

urlpatterns = [
  url(r'^$', Image.as_view()),
]
