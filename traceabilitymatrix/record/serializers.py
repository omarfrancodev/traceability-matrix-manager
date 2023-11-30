from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'

    def create(self, validated_data):
        associatedProject = validated_data['associatedProject']
        projectName = associatedProject.name

        projectNameAbbr = ''.join([word[0].upper() for word in projectName.split()])
        
        existingRecordsCount = Record.objects.filter(
            associatedProject=associatedProject,
            sprint=validated_data['sprint']
        ).count()

        customProjectRecordId = f"{projectNameAbbr}-S-{validated_data['sprint']}-{existingRecordsCount + 1:03d}"

        validated_data['projectRecordId'] = customProjectRecordId
        return super().create(validated_data)