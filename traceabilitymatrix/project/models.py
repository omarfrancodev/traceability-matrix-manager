from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_users = models.ManyToManyField('user.User', related_name='%(class)s_assigned_projects', blank=True)
    associated_matrix = models.OneToOneField('matrix.Matrix', on_delete=models.CASCADE, related_name='%(class)s_associated_project', blank=True)
