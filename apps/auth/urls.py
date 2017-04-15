from django.conf.urls import url
from .views import magic_link_login


urlpatterns = [
    url(r'^magic-link/(?P<token>\w+)/', magic_link_login, name='auth-magic_link'),
]
