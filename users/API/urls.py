from django.urls import path, include

from .views import (
    SignUpAPIView, SignInAPIView, UserRetrieveUpdateAPIView, CustomRefreshTokenView
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('signup', SignUpAPIView.as_view()),
    path('signin', SignInAPIView.as_view()),
    path('current', UserRetrieveUpdateAPIView.as_view()),
    path('check/access_token', TokenVerifyView.as_view()),
    path('get/access_token', CustomRefreshTokenView.as_view()),
]
