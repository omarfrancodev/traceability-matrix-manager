from .models import User
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "password"]


class CustomUserSerializer(UserSerializer):
    assignedProjects = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta(UserSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "assignedProjects"]
