from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from django_currentuser.middleware import get_current_authenticated_user
from eventrecord.models import EventRecord

User = get_user_model()


@receiver(pre_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    current_user = get_current_authenticated_user()
    EventRecord.objects.create(
        actionType=EventRecord.Action.Delete,
        userFullNameExec=current_user.fullName,
        userRoleExec=current_user.role,
        modelAffected=User.__name__,
        data=f"Full Name: {instance.fullName} - Role: {instance.role}",
    )


@receiver(pre_save, sender=User)
def restrict_role_change(sender, instance, **kwargs):
    if instance.pk is not None:
        original_instance = User.objects.get(pk=instance.pk)
        current_user = get_current_authenticated_user()

        if original_instance.id != current_user.id and original_instance.role != instance.role:
            update_role_create_event_record(current_user, instance)
        elif original_instance.role != instance.role:
            if original_instance.role != User.Role.Admin:
                response_data = {
                    "message": "You do not have permission to perform this action. Changing the user role is not allowed for non-admin users."
                }
                raise PermissionDenied(response_data)
            update_role_create_event_record(original_instance, instance)


def update_role_create_event_record(current_user, instance):
    instance.groups.clear()
    assign_groups(instance, instance.role)
    EventRecord.objects.create(
        actionType=EventRecord.Action.EditRole,
        userFullNameExec=current_user.fullName,
        userRoleExec=current_user.role,
        modelAffected=User.__name__,
        data=f"Full Name: {instance.fullName} - New Role: {instance.role}",
    )


@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created, **kwargs):
    if created:
        role = instance.role
        assign_groups(instance, role)


def assign_groups(instance, role):
    grp = " Group"
    if role == User.Role.Admin:
        group = Group.objects.get(name=User.Role.Admin + grp)
        instance.groups.add(group)
    elif role == User.Role.TeamMember:
        group = Group.objects.get(name=User.Role.TeamMember + grp)
        instance.groups.add(group)
    elif role == User.Role.Guest:
        group = Group.objects.get(name=User.Role.Guest + grp)
        instance.groups.add(group)
