from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from project.serializers import ProjectSerializer
from project.models import Project

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "password"]


class CustomUserSerializer(UserSerializer):
    myProjects = ProjectSerializer(many=True, read_only=True)
    assignedProjects = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_empty=True,
    )
    otherProjects = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "myProjects", "otherProjects", "assignedProjects"]
    
    def get_otherProjects(self, instance):
        assignedProjectIds = instance.myProjects.values_list("id", flat=True)
        other_projects = Project.objects.exclude(id__in=assignedProjectIds)
        return ProjectSerializer(other_projects, many=True).data
    
    def update(self, instance, validated_data):
        assignedProjectIds = validated_data.pop("assignedProjects", [])
        instance = super().update(instance, validated_data)
        if assignedProjectIds:
            instance.myProjects.set(assignedProjectIds)
        
        return instance