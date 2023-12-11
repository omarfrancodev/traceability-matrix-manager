from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    isPublished = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=255, blank=True)
    recordIdValues = models.IntegerField(default=0)