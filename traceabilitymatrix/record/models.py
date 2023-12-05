from django.db import models
from project.models import Project
from django_currentuser.db.models import CurrentUserField


class Record(models.Model):
    class Phase(models.TextChoices):
        Approval = "Approval", "Approval"
        Initiation = "Initiation", "Initiation"
        Development = "Development", "Development"

    class Status(models.TextChoices):
        Proposed = "Proposed", "Proposed"
        Implemented = "Implemented", "Implemented"
        Verifying = "Verifying", "Verifying"
        Approved = "Approved", "Approved"

    class Impact(models.TextChoices):
        NA = "NA", "NA"
        Low = "Low", "Low"
        Medium = "Medium", "Medium"
        High = "High", "High"

    associatedProject = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="associatedRecords"
    )
    projectRecordId = models.CharField(max_length=255, blank=True)
    sprint = models.CharField(max_length=255)
    phase = models.CharField(max_length=25, choices=Phase.choices)
    type = models.CharField(max_length=255)
    artifactName = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    keyRelationship = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=Status.choices)
    createdBy = CurrentUserField(related_name="createdRecordBy")
    modifiedBy = CurrentUserField(on_update=True, related_name="modifiedRecordsBy")
    creationDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now=True)
    impact = models.CharField(max_length=25, choices=Impact.choices)
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
