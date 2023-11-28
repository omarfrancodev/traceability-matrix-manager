from django.db import models

class Matrix(models.Model):
    associatedProject = models.OneToOneField('project.Project', on_delete=models.CASCADE, related_name='%(class)s_associatedMatrix')
