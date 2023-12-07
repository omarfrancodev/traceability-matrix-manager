from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django_currentuser.middleware import get_current_authenticated_user
from eventrecord.models import EventRecord
from .models import Record
import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=Record)
def record_deleted(sender, instance, **kwargs):
    current_user = get_current_authenticated_user()
    EventRecord.objects.create(
        actionType=EventRecord.Action.Delete,
        userFullNameExec=current_user.fullName,
        userRoleExec=current_user.role,
        appModel=Record.__name__,
    )

@receiver(pre_save, sender=Record)
def generate_project_record_id(sender, instance, **kwargs):
    associatedProject = instance.associatedProject
    projectName = associatedProject.name
    projectNameAbbr = "".join([word[0].upper() for word in projectName.split()])

    existingRecordsCount = Record.objects.filter(
        associatedProject=associatedProject, sprint=instance.sprint
    ).count()
    
    customProjectRecordId = (
        f"{projectNameAbbr}-S-{instance.sprint}-{existingRecordsCount + 1:03d}"
    )

    instance.projectRecordId = customProjectRecordId


@receiver(pre_save, sender=Record)
def validate_key_relationship(sender, instance, **kwargs):
    if instance.keyRelationship == "NA":
        return

    existingRecords = Record.objects.filter(
        associatedProject=instance.associatedProject
    ).exclude(pk=instance.pk)
    matchingCustomProjectIds = existingRecords.values_list("projectRecordId", flat=True)

    if instance.keyRelationship not in matchingCustomProjectIds:
        raise ValidationError(
            'El valor de keyRelationship debe ser igual a uno de los projectRecordId existentes o "NA"'
        )


@receiver(post_delete, sender=Record)
def delete_record_file(sender, instance, **kwargs):
    resources = instance.files.all()

    for resource in resources:
        if resource.file and os.path.isfile(resource.file.path):
            os.remove(resource.file.path)
