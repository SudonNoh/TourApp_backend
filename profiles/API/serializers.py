from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(max_length=128, required=True)
    profile_img = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'username',
            'birth',
            'profile_img',
            'introduce'
        ]
        
    def get_profile_img(self, obj):
        if obj.profile_img:
            return obj.profile_img
        
        return 'https://static.productionready.io/images/smiley-cyrus.jpg'