from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView

from profiles.models import Profile
from .serializers import ProfileSerializer

# Create your views here.
# class ProfileRetrieveAPIView(RetrieveAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Profile.objects.select_related('user')
#     serializer_class = ProfileSerializer
    
#     def retrieve(self, request, *args, **kwargs):
#         print(request.user.email)
#         try:
#             profile = self.queryset.get(user__email=request.user.email)
#         except Profile.DoesNotExist:
#             raise NotFound('A profile with this email does not exist.')
        
#         serializer = self.serializer_class(
#             profile,
#             context = {
#                 request:request
#             }
#         )
        
#         return Response(serializer.data, status=status.HTTP_200_OK)
