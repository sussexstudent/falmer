from django.urls import path

from .views import magic_link_login, sso, logout_view, email_link_request, email_link_sent, generate_jwt, me

urlpatterns = [
    path('logout/', logout_view, name='auth-logout'),
    path('login-request/', email_link_request, name='auth-request'),
    path('login-sent/', email_link_sent, name='auth-request-sent'),
    path('magic-link/<slug:token>/', magic_link_login, name='auth-magic_link'),
    path('token/', generate_jwt, name='auth-magic_link'),
    path('me/', me, name='auth-magic_link'),
    path('sso/', sso, name='auth-sso'),
]
