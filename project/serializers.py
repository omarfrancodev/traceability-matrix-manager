from rest_framework import serializers
from .models import Project
from record.serializers import RecordSerializer
from django_currentuser.middleware import get_current_authenticated_user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "isPublished", "createdBy"]

    def create(self, validated_data):
        current_user = get_current_authenticated_user()
        project = Project.objects.create(
            createdBy=current_user.fullName, **validated_data
        )

        return project


class DetailProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "createdBy",
            "isPublished",
            "createdAt",
            "updatedAt",
        ]


class DetailProjectRecordSerializer(serializers.ModelSerializer):
    associatedRecords = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "associatedRecords"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["associatedRecords"] = sorted(
            data["associatedRecords"], key=lambda x: x["id"]
        )
        return data


class DetailUsersProjectSerializer(serializers.ModelSerializer):
    assignedUsers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="fullName"
    )

    class Meta:
        model = Project
        fields = ["id", "name", "createdBy", "assignedUsers"]
