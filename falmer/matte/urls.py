from django.urls import path

from .views import Image

urlpatterns = [
  path('', Image.as_view()),
]
