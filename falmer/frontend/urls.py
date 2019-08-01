from django.urls import path, re_path

from .views import application_serve, FrontendAPI


urlpatterns = [
    path('frontend/', FrontendAPI.as_view()),
    re_path(r'^$', application_serve, name='frontend'),
    re_path(r'^.*/$', application_serve),
]
