from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assignedUsers = models.ManyToManyField('user.User', related_name='%(class)s_assignedProjects', blank=True)
    associatedMatrix = models.OneToOneField('matrix.Matrix', on_delete=models.CASCADE, related_name='%(class)s_associatedProject', blank=True)
