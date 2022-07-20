from unittest.util import _MAX_LENGTH
from wsgiref import validate
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


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
            
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'],)
        
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
    mobile = serializers.CharField(
        max_length = 11
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'mobile',
            'last_login'
        ]
        
    def update(self, instance, validated_data):
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        
        return instance