from django.urls import path

from .views import application_serve, FrontendAPI


urlpatterns = [
    path('frontend/', FrontendAPI.as_view()),
    path('<path:path>', application_serve),
]
