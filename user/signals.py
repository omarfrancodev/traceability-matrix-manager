from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


@receiver(pre_save, sender=User)
def restrict_role_change(sender, instance, **kwargs):
    if instance.pk is not None:
        originalInstance = User.objects.get(pk=instance.pk)
        if originalInstance.role != instance.role:
            response_data = {"message": "Changing user role is not allowed."}
            raise PermissionDenied(response_data)


@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created, **kwargs):
    grp = " Group"
    if created:
        role = instance.role

        if role == User.Role.Admin:
            group = Group.objects.get(name=User.Role.Admin + grp)
            instance.groups.add(group)
        elif role == User.Role.TeamMember:
            group = Group.objects.get(name=User.Role.TeamMember + grp)
            instance.groups.add(group)
        elif role == User.Role.Guest:
            group = Group.objects.get(name=User.Role.Guest + grp)
            instance.groups.add(group)
