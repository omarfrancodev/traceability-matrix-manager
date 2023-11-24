from django.db import models
from matrix.models import Matrix

class Record(models.Model):
    associatedMatrix = models.ForeignKey(Matrix, on_delete=models.CASCADE, related_name='associatedRecords')
    customProjectId = models.CharField(max_length=255)
    sprint = models.CharField(max_length=255)
    artifact_name = models.CharField(max_length=255)
    urlResource = models.URLField(null=True, blank=True)
    locationResource = models.FileField(upload_to='media/', null=True, blank=True)
    keyRelationship = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    responsible = models.CharField(max_length=255)
    creationDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now=True)
    impact = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
