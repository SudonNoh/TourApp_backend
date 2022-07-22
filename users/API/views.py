from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    SignInSerialzier, SignUpSerializer, UserSerializer, CustomRefreshTokenSerializer
)


class SignUpAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SignInAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerialzier

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user_data = request.data
        profile_data = request.data.get('profile', {})

        serializer_data = {
            'email': user_data.get('email', request.user.email),
            'mobile': user_data.get('mobile', request.user.mobile),

            'profile': {
                'username': profile_data.get('username', request.user.profile.username),
                'birth': profile_data.get('birth', request.user.profile.birth),
                'profile_img': user_data.get('profile_img', request.user.profile.profile_img),
                'introduce': profile_data.get('introduce', request.user.profile.introduce),
            }
        }
        
        print(serializer_data)
        
        serializer = self.serializer_class(
            request.user, serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomRefreshTokenView(TokenRefreshView):
    serializer_class = CustomRefreshTokenSerializer
