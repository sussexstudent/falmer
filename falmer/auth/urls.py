from django.conf.urls import url
from .views import magic_link_login, logout_view, email_link_request, email_link_sent

urlpatterns = [
    url(r'^logout/', logout_view, name='auth-logout'),
    url(r'^login-request/', email_link_request, name='auth-request'),
    url(r'^login-sent/', email_link_sent, name='auth-request-sent'),
    url(r'^magic-link/(?P<token>\w+)/', magic_link_login, name='auth-magic_link'),
]
