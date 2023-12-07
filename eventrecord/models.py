from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class EventRecord(models.Model):
    class Action(models.TextChoices):
        Delete = "Delete", "Delete"
        EditRole = "Edit Role", "Edit Role"
        Login = "Login", "Login"

    actionType = models.CharField(max_length=10, choices=Action.choices)
    userFullNameExec = models.CharField(max_length=255, blank=True)
    userFullNameAffected = models.CharField(max_length=255, blank=True)
    userRoleExec = models.CharField(max_length=50, blank=True)
    userRoleAffected = models.CharField(max_length=50, blank=True)
    appModel = models.CharField(max_length=255, blank=True)
    serverTimestamp = models.DateTimeField(auto_now_add=True)
    clientLocalTimestamp = models.DateTimeField(blank=True)
    
    REQUIRED_FIELDS = ["actionType"]

    def save(self, *args, **kwargs):
        self.clientLocalTimestamp = timezone.localtime(self.serverTimestamp)
        super().save(*args, **kwargs)
