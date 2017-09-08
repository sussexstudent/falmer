from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import LinkRenderer


urlpatterns = [
    url(r'^(?P<model>\w+)/(?P<pk>\w+)/', LinkRenderer.as_view()),
]
