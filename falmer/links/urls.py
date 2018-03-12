from django.urls import path

from .views import LinkRenderer


urlpatterns = [
    path('<str:model>/<int:pk>/', LinkRenderer.as_view()),
]
