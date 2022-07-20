from django.urls import path, include

from .views import SignUpAPIView, SignInAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('signup', SignUpAPIView.as_view()),
    path('signin', SignInAPIView.as_view()),
    path('current', UserRetrieveUpdateAPIView.as_view()),
]