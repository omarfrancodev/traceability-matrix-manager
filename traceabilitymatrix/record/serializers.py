from rest_framework import serializers
from .models import Record, ResourceURL, ResourceFile


class ResourceURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceURL
        fields = ["url"]


class ResourceFileSerializer(serializers.Serializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ResourceFile
        fields = ["file_url"]

    def get_file_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.file.url)


class RecordSerializer(serializers.ModelSerializer):
    urls = ResourceURLSerializer(many=True, read_only=True)
    files = ResourceFileSerializer(many=True, read_only=True)

    uploadedFiles = serializers.ListField(
        child=serializers.FileField(
            max_length=10000, allow_empty_file=True
        ),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    uploadedURLs = serializers.ListField(
        child=serializers.URLField(max_length=10000, allow_blank=True),
        write_only=True,
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = Record
        fields = [
            "id",
            "associatedProject",
            "projectRecordId",
            "sprint",
            "artifactName",
            "keyRelationship",
            "status",
            "createdBy",
            "modifiedBy",
            "creationDate",
            "updateDate",
            "impact",
            "notes",
            "files",
            "urls",
            "uploadedFiles",
            "uploadedURLs",
        ]

    def create(self, validated_data):
        uploadedFiles = validated_data.pop("uploadedFiles", [])
        uploadedURLs = validated_data.pop("uploadedURLs", [])
        record = Record.objects.create(**validated_data)
        if uploadedFiles:
            for file in uploadedFiles:
                if file:
                    ResourceFile.objects.create(record=record, file=file)

        if uploadedURLs:
            for url in uploadedURLs:
                if url:
                    ResourceURL.objects.create(record=record, url=url)

        return record
