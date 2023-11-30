from rest_framework import serializers
from .models import Project
from record.serializers import RecordSerializer
from user.serializers import ProjectUserDetailsSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']
        
class DetailProjectSerializer(serializers.ModelSerializer):
    associatedRecords = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'associatedRecords']

class DetailUsersProjectSerializer(serializers.ModelSerializer):
    assignedUsers = ProjectUserDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'assignedUsers']