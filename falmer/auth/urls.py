from django.conf.urls import url
from .views import magic_link_login, logout_view

urlpatterns = [
    url(r'^logout/', logout_view, name='auth-logout'),
    url(r'^magic-link/(?P<token>\w+)/', magic_link_login, name='auth-magic_link'),
]
