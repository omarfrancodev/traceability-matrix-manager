from rest_framework import serializers
from .models import Record, ResourceURL, ResourceFile
from django_currentuser.middleware import get_current_authenticated_user


class RecordSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    keyRelationships = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="projectRecordId"
    )
    recordRelations = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )
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
            "recordRelations",
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
        recordsRelated = None
        try:
            recordsRelated = validated_data.pop("recordRelations")
        except Exception:
            pass
        uploaded_files = validated_data.pop("uploadedFiles", [])
        uploaded_urls = validated_data.pop("uploadedURLs", [])
        record = Record.objects.create(
            createdBy=current_user.fullName,
            modifiedBy=current_user.fullName,
            **validated_data
        )
        if recordsRelated:
            record.keyRelationships.set(recordsRelated)

        for file in uploaded_files:
            if file:
                ResourceFile.objects.create(record=record, file=file)

        for url in uploaded_urls:
            if url:
                ResourceURL.objects.create(record=record, url=url)

        return record

    def update(self, instance, validated_data):
        current_user = get_current_authenticated_user()
        recordsRelated = validated_data.pop(
            "recordRelations", instance.keyRelationships.values_list("id", flat=True)
        )
        modifiedBy = current_user.fullName
        instance.modifiedBy = modifiedBy
        instance.keyRelationships.set(recordsRelated)

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        key_relationships = data.get("keyRelationships", [])
        data["keyRelationships"] = {
            "prev": [
                rel
                for rel in key_relationships
                if Record.objects.get(projectRecordId=rel).id < instance.id
            ],
            "post": [
                rel
                for rel in key_relationships
                if Record.objects.get(projectRecordId=rel).id > instance.id
            ],
        }
        return data


class NestedRecordSerializer(serializers.ModelSerializer):
    keyRelationships = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="projectRecordId"
    )

    class Meta:
        model = Record
        fields = [
            "id",
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
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        key_relationships = data.get("keyRelationships", [])
        data["keyRelationships"] = {
            "prev": [
                rel
                for rel in key_relationships
                if Record.objects.get(projectRecordId=rel).id < instance.id
            ],
            "post": [
                rel
                for rel in key_relationships
                if Record.objects.get(projectRecordId=rel).id > instance.id
            ],
        }
        return data


class RecordDetailSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    recordsPrev = NestedRecordSerializer(many=True, read_only=True)
    recordsPost = NestedRecordSerializer(many=True, read_only=True)

    keyRelationships = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="projectRecordId"
    )

    class Meta:
        model = Record
        fields = [
            "id",
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
            "recordsPrev",
            "recordsPost",
        ]

    def get_files(self, obj):
        files = ResourceFile.objects.filter(record=obj)
        return [self.get_file_url(file) for file in files]

    def get_file_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.file.url)

    def get_urls(self, obj):
        urls = ResourceURL.objects.filter(record=obj)
        return [url.url for url in urls]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        related_records = self._get_related_records(instance, instance.id)
        key_relationships = data.get("keyRelationships", [])
        data["keyRelationships"] = {
            "prev": [
                rel
                for rel in key_relationships
                if Record.objects.get(projectRecordId=rel).id < instance.id
            ],
            "post": [
                rel
                for rel in key_relationships
                if Record.objects.get(projectRecordId=rel).id > instance.id
            ],
        }
        data["recordsPrev"] = NestedRecordSerializer(
            related_records["recordsPrev"], many=True
        ).data
        data["recordsPost"] = NestedRecordSerializer(
            related_records["recordsPost"], many=True
        ).data
        return data

    def _get_related_records(
        self, instance, first_id, prev_records=None, post_records=None
    ):
        if prev_records is None:
            prev_records = set()
        if post_records is None:
            post_records = set()

        key_relationships = instance.keyRelationships.all()

        for related_record in key_relationships:
            if related_record.id != first_id:
                if (
                    related_record.id < instance.id
                    and related_record not in prev_records
                    and related_record not in post_records
                    and related_record.id < first_id
                ):
                    prev_records.add(related_record)
                    self._get_related_records(
                        related_record, first_id, prev_records, post_records
                    )
                elif (
                    related_record.id > instance.id
                    and related_record not in post_records
                    and related_record not in prev_records
                    and related_record.id > first_id
                ):
                    post_records.add(related_record)
                    self._get_related_records(
                        related_record, first_id, prev_records, post_records
                    )

        return {
            "recordsPrev": sorted(prev_records, key=lambda x: x.id),
            "recordsPost": sorted(post_records, key=lambda x: x.id),
        }
