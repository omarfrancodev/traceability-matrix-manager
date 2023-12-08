from rest_framework import serializers
from .models import Record, ResourceURL, ResourceFile
from django_currentuser.middleware import get_current_authenticated_user

class StringListField(serializers.ListField):
    child = serializers.CharField(min_length=2)

class RecordSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    keyRelationships = StringListField()

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
            "keyRelationships",
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
        current_user = get_current_authenticated_user()
        uploaded_files = validated_data.pop("uploadedFiles", [])
        uploaded_urls = validated_data.pop("uploadedURLs", [])
        record = Record.objects.create(
            createdBy=current_user.fullName,
            modifiedBy=current_user.fullName,
            **validated_data
        )

        for file in uploaded_files:
            if file:
                ResourceFile.objects.create(record=record, file=file)

        for url in uploaded_urls:
            if url:
                ResourceURL.objects.create(record=record, url=url)

        return record

    def update(self, instance, validated_data):
        current_user = get_current_authenticated_user()
        modifiedBy = current_user.fullName
        instance.modifiedBy = modifiedBy

        for field in instance._meta.fields:
            field_name = field.name
            if field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])

        uploadedFiles = validated_data.get("uploadedFiles")
        if uploadedFiles:
            self.update_relation(ResourceFile, instance, "file", uploadedFiles)

        uploadedUrls = validated_data.get("uploadedURLs")
        if uploadedUrls:
            self.update_relation(ResourceURL, instance, "url", uploadedUrls)

        instance.save()
        return instance

    def update_relation(self, model, instance, field_name, data):
        model.objects.filter(record=instance).delete()

        for newData in data:
            if newData:
                model.objects.create(record=instance, **{field_name: newData})

    def removing_simbols(self, string):
        charactersToDelete = "[]' "
        translationTable = str.maketrans("", "", charactersToDelete)
        chainWithoutSymbols = string.translate(translationTable)
        return chainWithoutSymbols
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        keyRelations = data["keyRelationships"]
        stringKeys = ""
        for key in keyRelations:
            stringKeys += key
        clean_relationships = self.removing_simbols(stringKeys)
        data["keyRelationships"] = clean_relationships.split(",")
        return data

class RecordDetailSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    associatedRecords = serializers.SerializerMethodField()

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
            "keyRelationships",
            "status",
            "createdBy",
            "modifiedBy",
            "createdAt",
            "updatedAt",
            "impact",
            "notes",
            "files",
            "urls",
            "associatedRecords",
        ]

    def get_files(self, obj):
        files = ResourceFile.objects.filter(record=obj)
        return [self.get_file_url(file) for file in files]

    def get_file_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.file.url)

    def get_urls(self, obj):
        urls = ResourceURL.objects.filter(record=obj)
        return [url.url for url in urls]

    def get_associatedRecords(self, obj):
        all_associated_records = []
        keyRelations = obj.keyRelationships
        if isinstance(keyRelations, str):
            clean_relationships = self.removing_simbols(keyRelations)
            keyRelations = clean_relationships.split(",")
        try:
            for keyRelation in keyRelations:
                related_record = Record.objects.get(projectRecordId=keyRelation)
                if related_record:
                    all_associated_records += self.get_all_associated_records(related_record)
        except Exception:
            pass
        serializer = RecordSerializer(all_associated_records, many=True)
        return serializer.data
    
    def get_all_associated_records(self, record):
        associated_records = [record]
        try:
            if record:
                keyRelations = record.keyRelationships
                if isinstance(keyRelations, str):
                    clean_relationships = self.removing_simbols(record.keyRelationships)
                    keyRelations = clean_relationships.split(",")
                if len(keyRelations) >= 1:
                    for keyRelation in keyRelations:
                        related_record = Record.objects.get(projectRecordId=keyRelation)
                        if related_record:
                            associated_records += self.get_all_associated_records(related_record)
        except Exception:
            pass
        return associated_records

    def removing_simbols(self, string):
        charactersToDelete = "[]' "
        translationTable = str.maketrans("", "", charactersToDelete)
        chainWithoutSymbols = string.translate(translationTable)
        return chainWithoutSymbols
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        keyRelations = data["keyRelationships"]
        stringKeys = ""
        for key in keyRelations:
            stringKeys += key
        clean_relationships = self.removing_simbols(stringKeys)
        data["keyRelationships"] = clean_relationships.split(",")
        return data