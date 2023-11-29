from django.db import models
from project.models import Project

class Record(models.Model):
    associatedProject = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='associatedRecords')
    customProjectId = models.CharField(max_length=255, blank=True)
    sprint = models.CharField(max_length=255)
    artifactName = models.CharField(max_length=255)
    urlResource = models.URLField(null=True, blank=True)
    locationResource = models.FileField(upload_to='files/', null=True, blank=True)
    keyRelationship = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    responsible = models.CharField(max_length=255)
    creationDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now=True)
    impact = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
