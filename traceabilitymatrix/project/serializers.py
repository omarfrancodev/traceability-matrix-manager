from rest_framework import serializers
from .models import Project
from record.serializers import RecordSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']
        
class DetailProjectSerializer(serializers.ModelSerializer):
    associatedRecords = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'associatedRecords']

class DetailUsersProjectSerializer(serializers.ModelSerializer):
    assignedUsers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="fullName")

    class Meta:
        model = Project
        fields = ['id', 'name', 'assignedUsers']