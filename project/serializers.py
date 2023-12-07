from rest_framework import serializers
from .models import Project
from record.serializers import RecordSerializer


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field="fullName")

    class Meta:
        model = Project
        fields = ["id", "name", "description", "isPublished", "owner"]


class DetailProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field="fullName")

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "owner",
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
        data['associatedRecords'] = sorted(data['associatedRecords'], key=lambda x: x['id'])
        return data


class DetailUsersProjectSerializer(serializers.ModelSerializer):
    assignedUsers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="fullName"
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field="fullName")

    class Meta:
        model = Project
        fields = ["id", "name", "owner", "assignedUsers"]
