from django.db import models
from project.models import Project

class Matrix(models.Model):
    associatedProject = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='%(class)s_associatedMatrix')
