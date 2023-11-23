from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    assigned_projects = models.ManyToManyField('project.Project', related_name='%(class)s_assigned_users', blank=True)
