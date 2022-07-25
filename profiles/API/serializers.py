from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(max_length=128, required=True)
    profile_img = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'birth',
            'profile_img',
            'introduce'
        ]