from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from profiles.models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, email, *args, **kwargs):

        profile = Profile.objects.select_related('user').get(
            user__eamil=email
        )

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)