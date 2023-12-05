from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()


@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created, **kwargs):
    if created:
        role = instance.role

        if role == User.Role.Admin:
            group, created = Group.objects.get_or_create(name="Admin Group")
            permissions = Permission.objects.filter(
                codename__in=[
                    "view_project",
                    "add_project",
                    "change_project",
                    "delete_project",
                    "add_record",
                    "view_record",
                    "change_record",
                    "delete_record",
                    "view_user",
                    "add_user",
                    "change_user",
                    "delete_user",
                ]
            )
            group.permissions.set(permissions)
            instance.groups.add(group)

        elif role == User.Role.TeamMember:
            group, created = Group.objects.get_or_create(name="Team Member Group")
            permissions = Permission.objects.filter(
                codename__in=[
                    "view_project",
                    "view_record",
                    "change_project",
                    "add_record",
                    "change_record",
                    "delete_record",
                ]
            )
            group.permissions.set(permissions)
            instance.groups.add(group)
        elif role == User.Role.Guest:
            group, created = Group.objects.get_or_create(name="Guest Group")
            permissions = Permission.objects.filter(
                codename__in=["view_project", "view_record"]
            )
            group.permissions.set(permissions)
            instance.groups.add(group)
