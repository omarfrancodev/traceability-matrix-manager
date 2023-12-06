from rest_framework import serializers
from .models import Project
from record.serializers import RecordSerializer

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field="fullName")
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'isDraft', 'owner']
        
class DetailProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field="fullName")
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'isDraft', 'createdAt', 'updatedAt']

class DetailProjectRecordSerializer(serializers.ModelSerializer):
    associatedRecords = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'associatedRecords']

class DetailUsersProjectSerializer(serializers.ModelSerializer):
    assignedUsers = serializers.SlugRelatedField(many=True, read_only=True, slug_field="fullName")
    owner = serializers.SlugRelatedField(read_only=True, slug_field="fullName")

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'assignedUsers']