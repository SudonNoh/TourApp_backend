from django.urls import path

from .views import (
    RegistrationAPIView
)
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('api/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
