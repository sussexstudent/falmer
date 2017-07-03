from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import application_serve, FrontendAPI


urlpatterns = [
    url(r'^frontend/', FrontendAPI.as_view()),
    url(r'^.*/$', application_serve),
]
