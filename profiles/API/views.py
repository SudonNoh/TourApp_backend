from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView

from profiles.models import Profile
from .serializers import ProfileSerializer

# Create your views here.
# 여기서 ProfieRetrieve는 나를 포함한 다른 모두가 볼 수 있는 Profile이다.
# users에 있는 UserRetrieveUpdateView는 나만 볼 수 있는 정보이다.
class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            # url에서 받은 profile_id로 정보를 찾는다.
            profile = self.queryset.get(id=kwargs['profile_id'])
        except Profile.DoesNotExist:
            raise NotFound('A profile with this email does not exist.')
        serializer = self.serializer_class(
            profile,
            context = {
                'request':request
            }
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
