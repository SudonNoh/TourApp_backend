import requests

from rest_framework import renderers, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    RegistrationSerializer,
)

# from ..models import User
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # user = User.objects.get(email=user['email'])
        # access_token = AccessToken.for_user(user)
        # refresh_token = RefreshToken.for_user(user)
        # tokens = {'access_token':access_token, 'refresh_token':refresh_token}

        return Response(serializer.data, status=status.HTTP_201_CREATED)
