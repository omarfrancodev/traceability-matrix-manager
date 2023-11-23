from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from dj_rest_auth.utils import jwt_encode

class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if user:
                attrs['user'] = user
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg)

        return attrs

    def get_token(self, user):
        return jwt_encode(user)