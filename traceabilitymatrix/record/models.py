from django.db import models
from matrix.models import Matrix

class Record(models.Model):
    associated_matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE, related_name='associated_records')
    custom_project_id = models.CharField(max_length=255)
    sprint = models.CharField(max_length=255)
    artifact_name = models.CharField(max_length=255)
    url_resource = models.URLField(null=True, blank=True)
    location_resource = models.FileField(upload_to='uploads/', null=True, blank=True)
    key_relationship = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    responsible = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    impact = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
