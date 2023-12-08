from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from eventrecord.models import EventRecord
from django_currentuser.middleware import get_current_authenticated_user
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(pre_delete, sender=Project)
def project_deleted(sender, instance, **kwargs):
    current_user = get_current_authenticated_user()
    EventRecord.objects.create(
        actionType=EventRecord.Action.Delete,
        userFullNameExec=current_user.fullName,
        userRoleExec=current_user.role,
        appModel=Project.__name__,
    )


@receiver(post_save, sender=Project)
def assign_project_to_user(sender, instance, created, **kwargs):
    if created:
        current_user = get_current_authenticated_user()
        assignedProjectIds = list(current_user.myProjects.values_list("id", flat=True))
        assignedProjectIds.append(instance.id)
        current_user.myProjects.set(assignedProjectIds)
        current_user.save()