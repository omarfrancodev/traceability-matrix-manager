from django.db import models
from django_currentuser.db.models import CurrentUserField

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    isPublished = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    owner = CurrentUserField(related_name="owner")