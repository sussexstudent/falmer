from django.urls import path

from .views import launcher


urlpatterns = [
  path('', launcher, name='launcher'),
]
