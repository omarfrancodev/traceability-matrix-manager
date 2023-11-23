from django.db import models
from project.models import Project

class Matrix(models.Model):
    associated_project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='%(class)s_associated_matrix')
