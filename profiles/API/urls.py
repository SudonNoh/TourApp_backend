from django.urls import path, include

from .views import ProfileRetrieveAPIView


urlpatterns = [
    path('<str:email>', ProfileRetrieveAPIView.as_view()),
]
