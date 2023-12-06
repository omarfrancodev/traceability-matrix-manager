from rest_framework import serializers
from .models import Record, ResourceURL, ResourceFile


class RecordSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    createdBy = serializers.SlugRelatedField(read_only=True, slug_field="fullName")
    modifiedBy = serializers.SlugRelatedField(read_only=True, slug_field="fullName")

    uploadedFiles = serializers.ListField(
        child=serializers.FileField(max_length=10000, allow_empty_file=True),
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
            "phase",
            "type",
            "artifactName",
            "description",
            "keyRelationship",
            "status",
            "createdBy",
            "modifiedBy",
            "createdAt",
            "updatedAt",
            "impact",
            "notes",
            "files",
            "urls",
            "uploadedFiles",
            "uploadedURLs",
        ]

    def get_files(self, obj):
        files = ResourceFile.objects.filter(record=obj)
        return [self.get_file_url(file) for file in files]

    def get_file_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.file.url)

    def get_urls(self, obj):
        urls = ResourceURL.objects.filter(record=obj)
        return [url.url for url in urls]

    def create(self, validated_data):
        uploaded_files = validated_data.pop("uploadedFiles", [])
        uploaded_urls = validated_data.pop("uploadedURLs", [])
        record = Record.objects.create(**validated_data)

        for file in uploaded_files:
            if file:
                ResourceFile.objects.create(record=record, file=file)

        for url in uploaded_urls:
            if url:
                ResourceURL.objects.create(record=record, url=url)

        return record
    
    def update(self, instance, validated_data):
        for field in instance._meta.fields:
            field_name = field.name
            if field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
                
        uploadedFiles = validated_data.get("uploadedFiles", [])
        self.update_relation(ResourceFile, instance, "file", uploadedFiles)

        uploadedUrls = validated_data.get("uploadedURLs", [])
        self.update_relation(ResourceURL, instance, "url", uploadedUrls)

        instance.save()
        return instance

    def update_relation(self, model, instance, field_name, data):
        model.objects.filter(record=instance).delete()

        for newData in data:
            if newData:
                model.objects.create(record=instance, **{field_name: newData})