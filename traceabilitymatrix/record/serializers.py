from rest_framework import serializers
from .models import Record
from django.utils.text import slugify

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'

    def create(self, validated_data):
        associated_project = validated_data['associatedProject']
        project_name = associated_project.name

        project_name_abbr = ''.join([word[0].upper() for word in project_name.split()])
        
        existing_records_count = Record.objects.filter(
            associatedProject=associated_project,
            sprint=validated_data['sprint']
        ).count()

        custom_project_id = f"{project_name_abbr}-S-{validated_data['sprint']}-{existing_records_count + 1:03d}"

        validated_data['customProjectId'] = custom_project_id
        return super().create(validated_data)