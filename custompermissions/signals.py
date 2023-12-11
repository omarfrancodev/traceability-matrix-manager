from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    grp = " Group"
    adminGroup, _ = Group.objects.get_or_create(name=User.Role.Admin + grp)
    teamMemberGroup, _ = Group.objects.get_or_create(name=User.Role.TeamMember + grp)
    guestGroup, _ = Group.objects.get_or_create(name=User.Role.Guest + grp)

    permissionsAdmin = Permission.objects.filter(
        codename__in=[
            "view_eventrecord",
            "add_eventrecord",
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
    adminGroup.permissions.set(permissionsAdmin)

    permissionsTM = Permission.objects.filter(
        codename__in=[
            "view_eventrecord",
            "add_eventrecord",
            "view_project",
            "view_record",
            "add_record",
            "change_record",
            "delete_record",
        ]
    )
    teamMemberGroup.permissions.set(permissionsTM)

    permissionsGuest = Permission.objects.filter(
        codename__in=[
            "view_eventrecord",
            "add_eventrecord",
            "view_project",
            "view_record",
        ]
    )
    guestGroup.permissions.set(permissionsGuest)