from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from Users.models import User
import logging

logger = logging.getLogger('main')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'user_name', 'first_name', 'last_name', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        user_name = attrs.get('user_name', '')
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        if not user_name.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        logger.info(f"Using serializer to register - {validated_data.get('user_name', '')}")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        logger.info(f'Returning refresh and access tokens for user {user.id}')
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['password', 'email', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            logger.error('Invalid credentials, try again')
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            logger.error('Account disabled, contact admin')
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'user_name': user.user_name,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as error:
            logger.error(error)
            return error
