from django.urls import path, include
from .views import ProfileRetrieveAPIView


urlpatterns = [
    path('<str:profile_id>', ProfileRetrieveAPIView.as_view())
    ]
