from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from project.serializers import ProjectSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "password"]


class CustomUserSerializer(UserSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    assignedProjects = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_empty=True,
    )
    
    class Meta(UserSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "projects", "assignedProjects"]
    
    def update(self, instance, validated_data):
        assignedProjectIds = validated_data.pop("assignedProjects", [])
        instance = super().update(instance, validated_data)
        if assignedProjectIds:
            instance.projects.set(assignedProjectIds)
        
        return instance