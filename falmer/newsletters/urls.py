from django.urls import path

from .views import ListMembersAPIView

urlpatterns = [
    path('<slug:list_slug>/members', ListMembersAPIView.as_view()),
]
