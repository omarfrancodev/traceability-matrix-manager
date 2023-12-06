from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    class Role(models.TextChoices):
        Admin = "Admin", "Admin"
        TeamMember = "Team Member", "Team Member"
        Guest = "Guest", "Guest"

    role = models.CharField(max_length=50, choices=Role.choices)
    fullName = models.CharField(max_length=255)
    email = models.EmailField(unique=True, verbose_name="Email Address")
    myProjects = models.ManyToManyField(
        "project.Project", related_name="assignedUsers", blank=True
    )
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullName","role", "username", "password"]

    objects = UserManager()