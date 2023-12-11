from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django_currentuser.middleware import get_current_authenticated_user
from eventrecord.models import EventRecord
from project.models import Project
from .models import Record
import os


@receiver(pre_delete, sender=Record)
def record_deleted(sender, instance, **kwargs):
    resources = instance.files.all()
    for resource in resources:
        if resource.file and os.path.isfile(resource.file.path):
            os.remove(resource.file.path)

    current_user = get_current_authenticated_user()
    EventRecord.objects.create(
        actionType=EventRecord.Action.Delete,
        userFullNameExec=current_user.fullName,
        userRoleExec=current_user.role,
        modelAffected=Record.__name__,
        data=f"ProjectRecordId: {instance.projectRecordId} - Artifact Name: {instance.artifactName}",
    )


@receiver(post_save, sender=Record)
def generate_project_record_id(sender, instance, created, **kwargs):
    if created:
        associatedProject = instance.associatedProject
        projectName = associatedProject.name
        projectNameAbbr = "".join([word[0].upper() for word in projectName.split()])

        project = Project.objects.get(id=associatedProject.id)
        existingValuesIds = project.recordIdValues + 1
        customProjectRecordId = (
            f"{projectNameAbbr}-S-{instance.sprint}-{existingValuesIds:03d}"
        )
        print(customProjectRecordId)

        instance.projectRecordId = customProjectRecordId
        instance.save()
        project.recordIdValues = existingValuesIds
        project.save()
