from rest_framework import serializers
from django.db.models import Q
from djoser.serializers import UserCreateSerializer, UserSerializer
from project.serializers import ProjectSerializer
from project.models import Project
from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "fullName", "email", "role", "password"]


class CustomListUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "fullName", "email", "role"]


class CustomUserSerializer(UserSerializer):
    myProjects = ProjectSerializer(many=True, read_only=True)
    assignedProjects = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_empty=True,
    )
    otherProjects = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = [
            "id",
            "fullName",
            "email",
            "role",
            "myProjects",
            "otherProjects",
            "assignedProjects",
        ]

    def get_otherProjects(self, instance):
        assignedProjectIds = instance.myProjects.values_list("id", flat=True)
        role = instance.role
        if role == User.Role.Admin:
            other_projects = Project.objects.filter(~Q(id__in=assignedProjectIds))
        else:
            other_projects = Project.objects.filter(
                ~Q(id__in=assignedProjectIds), isPublished=True
            )
        return ProjectSerializer(other_projects, many=True).data

    def update(self, instance, validated_data):
        assignedProjectIds = validated_data.pop("assignedProjects", [])
        instance = super().update(instance, validated_data)
        instance.myProjects.set(assignedProjectIds)

        return instance
