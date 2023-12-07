from django.db.models.signals import pre_delete
from django.dispatch import receiver
from eventrecord.models import EventRecord
from django_currentuser.middleware import get_current_authenticated_user
from .models import Project

@receiver(pre_delete, sender=Project)
def project_deleted(sender, instance, **kwargs):
    current_user = get_current_authenticated_user()
    EventRecord.objects.create(
        actionType=EventRecord.Action.Delete,
        userFullNameExec=current_user.fullName,
        userRoleExec=current_user.role,
        appModel=Project.__name__,
    )