from rest_framework import serializers
from .models import Matrix
from record.models import Record
from record.serializers import RecordSerializer

class MatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matrix
        fields = ['id', 'associatedProject']
        
class CustomDetailMatrixSerializer(serializers.ModelSerializer):
    associatedRecords = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Matrix
        fields = '__all__'