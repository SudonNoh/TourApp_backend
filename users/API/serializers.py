from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from profiles.models import Profile

from users.models import User
from profiles.API.serializers import ProfileSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token':str(refresh),
        'access_token':str(refresh.access_token)
    }


class SignUpSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    token = serializers.JSONField(
        read_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'mobile',
            'password',
            'is_active',
            'token'
        ]
        
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        setattr(user, "token", get_tokens_for_user(user))
        setattr(user, "message", "Success SignUp")
        
        user.last_login = timezone.localtime()
        user.save(update_fields=['last_login'],)

        return user
    

class SignInSerialzier(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    last_login = serializers.DateTimeField(
        read_only=True
    )
    
    token = serializers.JSONField(
        read_only=True
    )
    
    def validate(self, data):
        
        email = data.get('email', None)
        password = data.get('password', None)
        
        if email is None:
            raise serializers.ValidationError(
                "Please input Email Address."
            )
        
        if password is None:
            raise serializers.ValidationError(
                "Please input password."
            )
            
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
            
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
            
        user.last_login = timezone.localtime()
        user.save(update_fields=['last_login'],)
        
        # refresh token??? ????????? ??????????????? ??????????????? ?????? ?????? ????????????.
        try:
            token = OutstandingToken.objects.filter(user_id=user.id).latest('created_at')
            # Signin ??? ??? ????????? ?????? refresh token??? expired date??? ????????? ?????? ???????????? token???
            # blacklist??? ???????????????.
            if token.expires_at > timezone.now():
                pre_refresh_token = RefreshToken(token.token)
                pre_refresh_token.blacklist()
            # ?????? expired date??? ?????? ???????????? ?????? refresh token??? ????????????.
        except OutstandingToken.DoesNotExist:
            # ?????? ????????? ??????
            pass
            
        setattr(user, 'token', get_tokens_for_user(user))
        
        return {
            'email':user.email,
            'last_login':user.last_login,
            'token':user.token,
            'message':'Success SignIn'
        }
        

class UserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    mobile = serializers.CharField(max_length = 11)
    
    # Profile ??????
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = [
            'email',
            'mobile',
            'last_login',
            'profile'
        ]
        
    def update(self, instance, validated_data):
        
        profile_data = validated_data.pop('profile', {})
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        
        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
            
        instance.profile.save()
        
        return instance


class CustomRefreshTokenSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        
        # refresh token ?????? user??? ????????? ????????????.
        pre_refresh_token = attrs.get("refresh", None)
        if pre_refresh_token is None:
            raise serializers.ValidationError(
                "It's not include refresh token."
            )
            
        refresh_token_obj = RefreshToken(pre_refresh_token)
        user_id = refresh_token_obj.get('user_id', None)
        
        if user_id is None:
            raise serializers.ValidationError(
                "A user with this token was not found."
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User is not matched with ID"
            )
        

        # ????????? ?????? refresh token??? blacklist??? ????????????.
        refresh = self.token_class(attrs["refresh"])

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass
        
        # ????????? refresh token??? access token??? ???????????????.
        return get_tokens_for_user(user)