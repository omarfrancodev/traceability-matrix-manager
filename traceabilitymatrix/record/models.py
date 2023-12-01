from django.db import models
from project.models import Project
from django_currentuser.db.models import CurrentUserField


class Record(models.Model):
    associatedProject = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="associatedRecords"
    )
    projectRecordId = models.CharField(max_length=255, blank=True)
    sprint = models.CharField(max_length=255)
    artifactName = models.CharField(max_length=255)
    keyRelationship = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    createdBy = CurrentUserField(related_name="createdRecordBy")
    modifiedBy = CurrentUserField(on_update=True, related_name="modifiedRecordsBy")
    creationDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now=True)
    impact = models.CharField(max_length=255)
    notes = models.TextField(blank=True)


class ResourceURL(models.Model):
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        related_name="urls",
        blank=True,
        null=True,
    )
    url = models.URLField(null=True, blank=True)


class ResourceFile(models.Model):
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        related_name="files",
        blank=True,
        null=True,
    )
    file = models.FileField(upload_to="files/", null=True, blank=True)
